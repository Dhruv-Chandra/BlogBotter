<style>
img {width:1000px;}
p, li {font-size: 20px;}
h3 {font-size: 27px;}
h4 {font-size: 24px;}
</style>

<h1>Blog Botter</h1>

<h3><b>Home Page:</b></h3>
<img title="HomePage" alt="HomePage" src="./images/HomePage.png">

<h3><b>Model Selection Capability:</b></h3>
<h4>Options:</h4>
<ul>
    <li><i>GPT-4.</li>
    <li>LLaMa.</li>
    <li>Gemini.</i></li>
</ul>
<img title="ModelSelect" alt="ModelSelect" src="./images/ModelSelect.png">


<h3><b>Giving 'Title' Input:</b></h3>
<p>Enables the <b>'Generate a Fresh Blog'</b> Button.</p> 
<img title="TitleInput" alt="TitleInput" src="./images/TitleInput.png">

<h3><b>Clicking on the 'Generate a Fresh Blog'</b> button:</h3>
<img title="TitleOutput" alt="TitleOutput" src="./images/GeneratingResponse.png">

<h3><b>Generating Blog as per the given 'Title':</b></h3>
<ul>
<li><p>Final Blog can be seen in the right section.</p></li>
<img title="TitleOutput" alt="TitleOutput" src="./images/TitleOutput.png">
<li><p>Generated Blog can be exported in an HTML or PDF format using the <b>"Export"</b> button.</p></li>
<img title="TitleOutputExport" alt="TitleOutputExport" src="./images/TitleOutputExport.png"></ul>


<h3><b>Giving a 'Self-Written Blog' along with the 'Title':</b></h3>
<p>Enables both the <b>'Generate a Fresh Blog'</b> and <b>'Improve the Above Blog'</b> Buttons.</p>
<img title="TitleInput" alt="TitleInput" src="./images/TitleBlogInput.png" >

<h3><b>Clicking on the 'Improve the Above Blog' button:</b></h3>
<img title="TitleOutput" alt="TitleOutput" src="./images/GeneratingResponseImprove.png">

<h3><b>Improving Blog as per the given 'Title' and 'Blog':</b></h3>
<ul>
<li><p>Improved Blog can be seen in the right section.</p></li>
<li><p>Using the title provided, a google search is being done and content for the Top 5 results is extracted and run through a <b>"WordNetlemmatizer"</b> in order to focus our new blog on the most frequently used 10 words.</p></li>
<img title="TitleOutput" alt="TitleOutput" src="./images/ImprovedOutput.png">
<li><p>Improved Blog can be exported in an HTML or PDF format using the <b>"Export"</b> button.</p></li>
<img title="TitleOutputExport" alt="TitleOutputExport" src="./images/TitleOutputExport.png">
