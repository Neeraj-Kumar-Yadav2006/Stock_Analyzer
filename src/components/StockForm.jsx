import React, {useState} from "react";

function StockForm({fetchReport}){

const [ticker,setTicker] = useState("");

return(

<div style={{textAlign:"center",marginTop:"30px"}}>

<input
type="text"
placeholder="Enter Stock (AAPL)"
value={ticker}
onChange={(e)=>setTicker(e.target.value)}
style={{padding:"10px",marginRight:"10px"}}
/>

<button
onClick={()=>fetchReport(ticker)}
style={{
padding:"10px 20px",
background:"green",
color:"white",
border:"none"
}}

>

Analyze </button>

</div>

);

}

export default StockForm;
