Design Lab
========
![alt tag](https://raw.github.com/GstarGface/hide-and-cheek-design-lab/master/static/images/screenshot.png)
<h3>Built by <a href="https://www.linkedin.com/in/georgiaglassie">Georgia Glassie</a></h3>
<h3><strong>The Project</strong></h3>
<h5>Design Lab is an application developed as an independent project during my Hackbright Fellowship. </h5> 
<h5>Leveraging Design Lab, upstart clothing designers can take the hassle out of the error-prone custom design process. Design Lab’s interactive interface allows shoppers to design their own custom-made yoga pants in real time.  

Yogi empowerment extends to length, style, fabric, color, custom sizing, and personalized embroidery. No more hiking up, pulling down, or bugging out! Build your dream yoga pants or scroll through our user-generated lookbook for some style-inspiration! 
Design Lab is scheduled to launch in September 2015 in collaboration with <a href="www.hide-cheek.com">Hide&Cheek</a> a small -batch clothing manufacturer based in LA </h5>
<h4> Key features include:</h4>
<ul>
  <li>Dynamically generated images that change according to cunsumers' style decisions.</li>
  <li>Non-caching images that persist between pages, keeping the current style visible to the customer.</li>
  <li>Admin portal for the shop manager owner to maintain their inventory database; add, edit and discontinue the product's styles, fabrics, colors, sizes, etc. </li>
  <li>Admin portal dashboard displaying Google Analytics Usage data.</li>
</ul>

<h3><strong>Technologies Used</strong></h3>
Design Lab is written in Python 2.7, JavaScript, and HTML5/CSS3 with the use of PostgreSQL, Flask, jQuery, AJAX/JSON, Jinja2, Bootstrap.js, and SQLAlchemy. The Admin portal utilizes the Flask-Admin library and highcharts.js The lookbook is generated with Instagram images. Shopping cart integration via Shopify. 

<h3><strong>Environment</strong></h3>

1) Clone the repository:

<pre><code>$ git clone https://github.com/GstarGface/hide-and-cheek-design-lab.git</code></pre>

2) Create and activate a virtual environment in the same directory: 

<pre><code>$ pip install virtualenv
$ virtualenv env
$ source env/bin/activate 
</code></pre>

3) Install the required packages using pip:

<pre><code>(env)$ pip install -r requirements.txt
</code></pre>
