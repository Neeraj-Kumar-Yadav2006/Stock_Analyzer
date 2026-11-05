import React, { useState } from "react";
import axios from "axios";
import jsPDF from "jspdf";
import {
LineChart,
Line,
XAxis,
YAxis,
CartesianGrid,
Tooltip,
ResponsiveContainer
} from "recharts";
import "./App.css";

function App() {

const [ticker, setTicker] = useState("");
const [data, setData] = useState(null);
const [loading, setLoading] = useState(false);
const [chartData, setChartData] = useState([]);

const [error, setError] = useState("");  

const analyzeStock = async () => {
  setError("");  // clear previous error

  if (!ticker || ticker.trim().length === 0) {
    setError("Please enter a valid ticker symbol (e.g. TSLA, AAPL)");
    return;
  }

  try {
    setLoading(true);
    const response = await axios.get(
      `http://127.0.0.1:8000/analyze/${ticker.trim().toUpperCase()}`
    );
    setData(response.data);
    setChartData(response.data.chart || []);
    setLoading(false);

  } catch (error) {
    console.error(error);
    setError("Please enter a valid ticker symbol (e.g. TSLA, AAPL)");
    setLoading(false);
  }
};
/*Download <pdf></pdf>*/
const downloadPDF = () => {
  const doc = new jsPDF();
  const margin = 10;
  const pageWidth = doc.internal.pageSize.getWidth();
  const maxWidth = pageWidth - margin * 2;
  let y = 15;

  // ── Title ──
  doc.setFontSize(18);
  doc.setFont("helvetica", "bold");
  doc.text("AI Financial Report", margin, y);
  y += 12;

  // ── Divider ──
  doc.setDrawColor(37, 99, 235);
  doc.setLineWidth(0.8);
  doc.line(margin, y, pageWidth - margin, y);
  y += 10;

  // ── Stock Metrics ──
  doc.setFontSize(13);
  doc.setFont("helvetica", "bold");
  doc.text("Stock Metrics", margin, y);
  y += 8;

  doc.setFontSize(11);
  doc.setFont("helvetica", "normal");
  doc.text(`Ticker:       ${data.ticker}`, margin, y); y += 7;
  doc.text(`Price:        $${data.price}`, margin, y); y += 7;
  doc.text(`RSI:          ${Number(data.indicators?.RSI).toFixed(2)}`, margin, y); y += 7;
  doc.text(`MA14:         $${data.indicators?.MA14}`, margin, y); y += 7;
  doc.text(`Volatility:   ${Number(data.indicators?.volatility).toFixed(4)}`, margin, y); y += 7;
  doc.text(`Signal:       ${data.signal?.signal}`, margin, y); y += 12;

  // ── Divider ──
  doc.setDrawColor(200, 200, 200);
  doc.setLineWidth(0.4);
  doc.line(margin, y, pageWidth - margin, y);
  y += 10;

  // ── Sentiment ──
  doc.setFontSize(13);
  doc.setFont("helvetica", "bold");
  doc.text("Market Sentiment", margin, y);
  y += 8;

  doc.setFontSize(11);
  doc.setFont("helvetica", "normal");
  doc.text(`Sentiment:         ${data.sentiment?.sentiment}`, margin, y); y += 7;
  doc.text(`Score:             ${data.sentiment?.score}`, margin, y); y += 7;
  doc.text(`Articles Analyzed: ${data.sentiment?.articles_analyzed}`, margin, y); y += 12;

  // ── Divider ──
  doc.setDrawColor(200, 200, 200);
  doc.line(margin, y, pageWidth - margin, y);
  y += 10;

  // ── AI Report ──
  doc.setFontSize(13);
  doc.setFont("helvetica", "bold");
  doc.text("AI Analysis Report", margin, y);
  y += 8;

  doc.setFontSize(10);
  doc.setFont("helvetica", "normal");
  // splitTextToSize fixes truncation — wraps long text
  const reportLines = doc.splitTextToSize(data.report || "", maxWidth);
  reportLines.forEach((line) => {
    if (y > 270) {          // new page if running out of space
      doc.addPage();
      y = 15;
    }
    doc.text(line, margin, y);
    y += 6;
  });

  y += 8;

  // ── Divider ──
  doc.setDrawColor(200, 200, 200);
  doc.line(margin, y, pageWidth - margin, y);
  y += 8;

  // ── Disclaimer ──
  doc.setFontSize(8);
  doc.setTextColor(150, 150, 150);
  doc.text(
    "Disclaimer: This report is AI-generated for educational purposes only. Not financial advice.",
    margin, y
  );

  doc.save(`${data.ticker}_report.pdf`);
};
return (

<div className="container">

<header className="header">

<h1>Financial Intelligence Agent Platform</h1>

<p>
AI powered stock analysis, sentiment detection and market intelligence
</p>

</header>
<div className="searchBox">

<input
type="text"
placeholder="Search Stock (AAPL, TSLA, MSFT)"
value={ticker}
onChange={(e) => setTicker(e.target.value)}
onKeyDown={(e) => {
  if (e.key === "Enter") {
    analyzeStock();
  }
}}
/>

<button onClick={analyzeStock}>
{loading ? "Analyzing..." : "Analyze"}
</button>

</div>

{/* ← ADD THIS RIGHT HERE */}
{error && (
  <p style={{ color: "red", textAlign: "center", marginTop: "8px" }}>
    ⚠️ {error}
  </p>
)}
{/* Welcome section */}

{!data && (

<div className="welcome">

<div className="infoCard">
<h3>📈 Market Analysis</h3>
<p>Analyze stock performance and financial metrics instantly.</p>
</div>

<div className="infoCard">
<h3>📰 News Intelligence</h3>
<p>AI reads news and detects positive or negative sentiment.</p>
</div>

<div className="infoCard">
<h3>🤖 AI Insights</h3>
<p>Get AI generated summary of stock performance.</p>
</div>

</div>

)}

{data && (

<>

{/* AI REPORT */}

<div className="card">

<h2>AI Stock Report</h2>

<p style={{ whiteSpace: "pre-line" }}>
  {data.report}
</p>
<button onClick={downloadPDF} className="downloadBtn">
  Download PDF
</button>
</div>

{/* CHART */}

<div className="chartBox">

<h2>Stock Price Chart</h2>

<ResponsiveContainer width="100%" height={300}>

<LineChart data={chartData}>

<CartesianGrid strokeDasharray="3 3" />

<XAxis dataKey="day" />

<YAxis 
  domain={[
    (dataMin) => dataMin - 5,
    (dataMax) => dataMax + 5
  ]}
/>

<Tooltip />

<Line
type="monotone"
dataKey="price"
stroke="#2563eb"
strokeWidth={3}
/>

</LineChart>

</ResponsiveContainer>

</div>

{/* DASHBOARD */}

<div className="dashboard">

<div className="card">

<h2>Stock Metrics</h2>

<p><b>Ticker:</b> {data.ticker}</p>
<p><b>Price:</b> ${data.price}</p>
<p><b>RSI:</b> {Number(data.indicators?.RSI).toFixed(2)}</p>
<p><b>Moving Avg (14):</b> {data.indicators?.MA14}</p>
<p><b>Volatility:</b> {Number(data.indicators?.volatility).toFixed(4)}</p>
<p><b>Signal:</b> {data.signal?.signal}</p>

</div>

<div className="card">

<h2>Market Sentiment</h2>

<p><b>Sentiment:</b> {data.sentiment?.sentiment}</p>
<p><b>Score:</b> {data.sentiment?.score}</p>
<p><b>Articles Analyzed:</b> {data.sentiment?.articles_analyzed}</p>

</div>

</div>

</>

)}

</div>

);

}


export default App;
