xquery version 3.1;
module namespace html = 'http://rs.tdwg.com/html';

declare function html:dwc()
{
<html>
   <head>
      <meta charset="utf-8"/>
      <title>Test genereated web page</title>
   </head>
   <body>
      <p>Here is some text</p>
   </body>
</html>
};

declare function html:tcadrt()
{
	<html>
  <head>
    <meta charset="utf-8"/>
    <title>TCADRT - Vanderbilt University Department of History of Art</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
   <link rel="icon" href="http://tcadrt.org/img/favicon.png" type="image/x-icon"></link>
   <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.4/cosmo/bootstrap.min.css"></link>
   <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css"></link>
   <link href="../css/tcadrt.css" rel="stylesheet"></link>
   <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
   <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
    <script src="../static/js/title.js"></script>
</head>

<body>

  <nav class="navbar navbar-default">
          <div class="container-fluid">
              <!-- Brand and toggle get grouped for better mobile display -->
              <div class="navbar-header">
              <a href="http://tcadrt.org/"><img src="../img/tcadrt-logo-vs.png" style="position: relative; left:-16; float:left; margin-left:0; margin-top: 0; margin-right:20px; margin-bottom:0px;" width="56px" height="50px"/></a>
                  <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                      data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                      <span class="sr-only">Toggle navigation</span>
                      <span class="icon-bar"></span>
                      <span class="icon-bar"></span>
                      <span class="icon-bar"></span>
                  </button>
                  <a class="navbar-brand" href="http://tcadrt.org/">Traditional Chinese Architecture Digital Research Tool</a>
              </div>
              <!-- Collect the nav links, forms, and other content for toggling -->
              <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                  <ul class="nav navbar-nav">
                      <li class="active"><a href="http://tcadrt.org/">Home <span class="sr-only"
                              >(current)</span></a></li>
                      <li><a href="http://tcadrt.org/tool">Tool</a></li>

                  </ul>
              </div><!-- /.navbar-collapse -->
          </div><!-- /.container-fluid -->
      </nav>

    <div class="container" style="margin-bottom: 50px;">
   
  <p><div class="featured_image"><img src="../img/Lingyansi-medium.jpg" id="home-image"/><br/><em>Pizhita (Pratyeka Pagoda)</em>, 1057 CE</div>The Traditional Chinese Architecture Digital Research Tool is, at its core, a digital image archive of the monumental architecture of pre-modern China. The dataset is focused on our earliest extant examples of timber-frame architecture in China, largely dating from the 8th-13th centuries, and includes information on construction techniques as well as stylistic features. The vast majority of these buildings were constructed for ritual purposes, therefore data on style and structure of the buildings, as well as epigraphic information on site concerning patronage, have the potential to enhance not only our understanding of the aesthetics of traditional Chinese architecture over time and space, but also our understanding of the trade networks, crafts traditions, and spiritual aspirations of people living in pre-modern China.</p>
   <p>Currently in active development, the Traditional Chinese Architecture Digital Research Tool will be a be a public, browser-based architectural history research website. To see an example of our trial site (set up with the help of Steve Baskauf) click on Tool in the navigation bar</p>
     <p> When complete the tool will consist of four parts: </p>
     <p>1. A linked open data (LOD) database of architectural complexes and individual structures searchable both by name of site (ancient and modern) and by technical terminology used to describe individual elements of single timber-frame buildings that are known to vary across regions. Search terms will be in Chinese (traditional and simplified scripts), pinyin Romanization of modern Mandarin, and English translation. </p>
     <p>2. A photo archive of images keyed into the search terms of the database. This archive is based on my own photographs of more than one hundred middle-period structures and the building complexes of which they are part. This will be supplemented with architectural drawings to further research and teaching.</p>
     <p>3. A digital mapping tool that will allow search results to be located on a map of modern China using U.S. Geological Survey public domain base maps. This will be linked to the photo archive to facilitate viewing of search results through the map interface.</p>
     <ul>
       <li>The mapping tool will make use of the Vanderbilt Historical Gazetteer app, an open source application developed locally at Vanderbilt.</li>
       <li>Map output will be available in digital and analog forms for peer-reviewed publication. Although the research tool is designed primarily to allow digital searching and mapping of Chinese architecture, results of that research will ultimately be published in both digital and analog forms. We acknowledge that digital tools are both portable and powerful, however static version of search results, in the form of a single pdf, or as part of an article or book are still critical for archiving. </li>
     </ul>
     <p>4. Photographs and transcriptions of epigraphic information found at a given site. Titles of stele inscriptions and donor names will be searchable using traditional Chinese characters.</p>


</div><!-- /.container -->

  <footer class="footer">
      <div class="container">
        <p>The <em>Traditional Chinese Architecture Digital Research Tool</em> project was made possible by these institutions and sponsors:</p>
        <div class="sponsors">
        <a href="https://www.neh.gov/" class="logo" target="_blank"><img src="../img/neh-logo.png"/></a>
        <a href="http://www.library.vanderbilt.edu/" class="logo" target="_blank"><img src="../img/heard-library-logo.png"/></a>
        <a href="http://www.grahamfoundation.org/" class="logo" target="_blank"><img src="../img/gf-logo.png"/></a>
        <a href="https://as.vanderbilt.edu/" class="logo" target="_blank"><img src="../img/vanderbilt-cas-logo.png"/></a>
        <a href="https://mellon.org/" class="logo" target="_blank"><img src="../img/mellon-logo.png"/></a>
        <a href="https://as.vanderbilt.edu/historyart/" class="logo" target="_blank"><img src="../img/hart-logo.png"/></a>
        </div>
      </div>
    </footer>
</body>
</html>


};

declare function html:tool()
{
<html>
<head>
<meta charset="utf-8"/>
<title>TCADRT - Vanderbilt University Department of History of Art</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="icon" href="http://tcadrt.org/img/favicon.png" type="image/x-icon"></link>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.4/cosmo/bootstrap.min.css"></link>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css"></link>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.0.3/dist/leaflet.css"></link>
<link href="../css/tcadrt.css" rel="stylesheet"></link>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
<script src="https://unpkg.com/leaflet@1.0.3/dist/leaflet.js"></script>
<script src="../static/js/title.js"></script>
</head>

<body>

  <nav class="navbar navbar-default">
          <div class="container-fluid">
              <!-- Brand and toggle get grouped for better mobile display -->
              <div class="navbar-header">
              <a href="http://tcadrt.org/"><img src="../img/tcadrt-logo-vs.png" style="position: relative; left:-16; float:left; margin-left:0; margin-top: 0; margin-right:20px; margin-bottom:0px;" width="56px" height="50px"/></a>
                  <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                      data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                      <span class="sr-only">Toggle navigation</span>
                      <span class="icon-bar"></span>
                      <span class="icon-bar"></span>
                      <span class="icon-bar"></span>
                  </button>
                  <a class="navbar-brand" href="http://tcadrt.org/">Traditional Chinese Architecture Digital Research Tool</a>
              </div>
              <!-- Collect the nav links, forms, and other content for toggling -->
              <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                  <ul class="nav navbar-nav">
                      <li ><a href="http://tcadrt.org/">Home <span class="sr-only"
                              >(current)</span></a></li>
                      <li class="active"><a href="http://tcadrt.org/tool">Tool</a></li>

                  </ul>
              </div><!-- /.navbar-collapse -->
          </div><!-- /.container-fluid -->
      </nav>

    <div class="container" style="margin-bottom: 50px;">

      <div class="starter-template">
          <div class="bs-component">
              <div>
                  <p><div class="featured_image"><img class="img-responsive" src="../img/tool-image.jpg" style="float:left; margin-right:35px; margin-bottom: 20px; width:400px; height:268;" /><br/><em>Baoguosi Daxiongbaodian (Mahavira Treasure Hall)</em>, 1013 CE</div>This is a beta version of of the Traditional Chinese Architecture Digital Research Tool (TCADRT) whose current main objective is to express the modeled metadata of Tracy Miller. The next iteration will include not only the ability to add to this dataset but also to make connections between building elements, geography, and time in ways that will be useful for researchers of Traditional Chinese Architecture. <br/>Linked images are (c) 2017 Tracy G. Miller CC BY-NC<br/>Read <a href="http://baskauf.blogspot.com/2016/11/sparql-based-web-app-to-find-chinese.html" target="_blank">this blog post</a> for details.<br/>Further information about <a href="https://as.vanderbilt.edu/historyart/people/miller.php">Tracy Miller</a>.</p>
              </div>
          </div>
      </div>
      <div class="clear"></div>
    <h1>Search</h1>
     <div class="form-horizontal input-group-addon">
    <!-- <form class="form-inline" role="form"> -->

        <div class="form-group">
            <label for="box0" class="col-sm-4 control-label" id="boxLabel0">Language/语言/語言</label>
            <div class="col-sm-5 radio-row">
               <!--  <select name="languageDropdown" id="box0" class="form-control">
                    <option value='en' selected='selected'>English</option>
                    <option value='zh-hans' >简体中文</option>
                    <option value='zh-hant' >繁体中文</option>
                </select> -->
                <input type="radio" id="radio-en" name="language_selected" value='en'>English</input>
                <input type="radio" id="radio-zh-hans"  name="language_selected"  value="zh-hans"> 简体中文</input>
                <input type="radio" id="radio-zh-hant"  name="language_selected"  value="zh-hant"> 繁体中文</input>
            </div>
        </div>

        <div class="form-group">
            <label for="box1" class="col-sm-4 control-label" id="boxLabel1">Province</label>
            <div class="col-sm-5">
                <select name="provinceDropdown" id="box1" class="form-control">
                    <option value='?province' selected='selected'>Any province/任何省份</option>
                </select>
            </div>
        </div>

        <div class="form-group">
            <label for="box3" class="col-sm-4 control-label" id="boxLabel3">Dynasty range for site</label>
            <div class="col-sm-5">
                <select name="dynastyDropdown" id="box3" class="form-control">
                    <option value='?dynasty' selected='selected'>Any dynasty/任何一个朝代</option>
                </select>
            </div>
        </div>

        <div class="form-group">
            <label for="box2" class="col-sm-4 control-label" id="boxLabel2">Historic site</label>
            <div class="col-sm-5">
                <select name="siteDropdown" id="box2" class="form-control">
                    <option value='?site' selected='selected'>Any temple/任何寺庙</option>
                </select>
            </div>
        </div>
<!-- 
        <div class="form-group">
            <label for="box4" class="col-sm-4 control-label">Category</label>
            <div class="col-sm-5">
                <select name="categoryDropdown" id="box4" class="form-control">
                    <option value='?category' selected='selected'>Any Anatomical Feature</option>
                </select>
            </div>
        </div>
-->
        <button type="submit" class="btn btn-default" id="searchButton">Search</button>
        <button type="submit" class="btn btn-default" id="resetButton">Reset</button>
        <i id="searchSpinner" class="fa fa-spinner fa-spin fa-lg"></i>
    </div>

    <h1>Results</h1>

    <!--Here is where the number of buildings gets inserted -->
    <div id="div2"></div>

  <!--Here is where the map gets inserted-->
    <div id="mapid"></div>

  <!--Here is where the info and images get inserted-->
    <div id="div1"></div>


  


    <!-- pagination -->
    <nav id="bioimagesPagination" class="hidden">
      <ul class="pagination">
        <li>
          <a href="#" aria-label="Previous">
            <span aria-hidden="true">&#171;</span>
          </a>
        </li>
        <li><a href="#">1</a></li>
        <li><a href="#">2</a></li>
        <li><a href="#">3</a></li>
        <li><a href="#">4</a></li>
        <li><a href="#">5</a></li>
        <li>
          <a href="#" aria-label="Next">
            <span aria-hidden="true">&#187;</span>
          </a>
        </li>
      </ul>
    </nav>

    </div><!-- /.container -->



    <footer class="footer">
      <div class="container">
        <p>The <em>Traditional Chinese Architecture Digital Research Tool</em> project was made possible by these institutions and sponsors:</p>
        <div class="sponsors">
        <a href="https://www.neh.gov/" class="logo" target="_blank"><img src="../img/neh-logo.png"/></a>
        <a href="http://www.library.vanderbilt.edu/" class="logo" target="_blank"><img src="../img/heard-library-logo.png"/></a>
        <a href="http://www.grahamfoundation.org/" class="logo" target="_blank"><img src="../img/gf-logo.png"/></a>
        <a href="https://as.vanderbilt.edu/" class="logo" target="_blank"><img src="../img/vanderbilt-cas-logo.png"/></a>
        <a href="https://mellon.org/" class="logo" target="_blank"><img src="../img/mellon-logo.png"/></a>
        <a href="https://as.vanderbilt.edu/historyart/" class="logo" target="_blank"><img src="../img/hart-logo.png"/></a>
        </div>
      </div>
       <!-- Note: I had to move this from the head to here because defining the variable mymap apparently must happen after the creation of the mapid div -->
      <script src="../js/tang-song.js"></script>
      <script src="../static/js/map.js"></script>

    </footer>

  </body>
</html>

  

};

