import React from "react";

function SummaryCard({summary}){

return(

<div style={{
margin:"40px auto",
width:"60%",
padding:"20px",
background:"#f4f4f4",
borderRadius:"10px"
}}>

<h2>AI Summary</h2>

<p>{summary}</p>

</div>

);

}

export default SummaryCard;
