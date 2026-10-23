"""Build the English blog and article pages from content/blog-posts.json."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
POSTS=json.loads((ROOT/'content/blog-posts.json').read_text())
BASE='https://danielleronit.com'
E=escape
HEADER='''<header class="site-header" dir="ltr" aria-label="Page header">
  <a class="site-brand" href="/">Danielle Ronit</a>
  <nav class="site-links" aria-label="Main navigation">
    <a href="/abundance/">The Abundance Healing Container</a>
    <a href="/IEMT/">1:1 Healing Sessions</a>
    <a href="/retreats/">Retreats</a>
    <a href="/testimonials/">Testimonials</a>
    <a href="/blog/" aria-current="page">Blog</a>
  </nav>
</header>'''
FOOTER='''<footer class="blog-footer"><a class="footer-brand" href="/">Danielle Ronit</a><nav aria-label="Footer navigation"><a href="/abundance/">The Abundance Healing Container</a><a href="/IEMT/">1:1 Healing Sessions</a><a href="/blog/">Blog</a><a href="mailto:danielleronit@gmail.com">danielleronit@gmail.com</a></nav></footer>'''
def document(title,description,path,body,schema,image=None):
 image=image or POSTS[0]['image']
 schema_json=json.dumps(schema,ensure_ascii=False).replace('</','<\\/')
 return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{E(title)} | Danielle Ronit</title>
  <meta name="description" content="{E(description,quote=True)}">
  <link rel="canonical" href="{BASE+path}">
  <meta property="og:title" content="{E(title,quote=True)}">
  <meta property="og:description" content="{E(description,quote=True)}">
  <meta property="og:url" content="{BASE+path}">
  <meta property="og:type" content="{'article' if path.startswith('/post/') else 'website'}">
  <meta property="og:image" content="{BASE+image}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&amp;family=Lato:wght@300;400;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/IEMT/style.css?v=iemt-moshe-1">
  <link rel="stylesheet" href="/assets/site-header.css?v=blog-3">
  <link rel="stylesheet" href="/assets/blog.css?v=1">
  <script type="application/ld+json">{schema_json}</script>
</head>
<body class="blog-page">
<a class="skip-link" href="#main">Skip to content</a>
{HEADER}
<main id="main">{body}</main>
{FOOTER}
</body>
</html>
'''
def url(p):return '/post/'+p['slug']+'/'
def excerpt(p,limit=185):
 text=re.sub(r'\s+',' ',p['excerpt']).strip()
 if len(text)>limit:text=text[:limit].rsplit(' ',1)[0].rstrip('.,')+'…'
 return text
def meta(p):return f'<p class="post-meta"><time datetime="{p["firstPublishedDate"]}">{E(p["displayDate"])}</time><span aria-hidden="true">·</span><span>{p["minutesToRead"]} min read</span></p>'
def card(p,featured=False):
 return f'''<article class="blog-card{' blog-featured' if featured else ''}">
  <a class="blog-image-link" href="{url(p)}" tabindex="-1" aria-hidden="true"><img src="{p['image']}" alt="" width="1000" height="750" {'fetchpriority="high"' if featured else 'loading="lazy"'}></a>
  <div class="blog-card-copy">{'<p class="blog-eyebrow">Latest story</p>' if featured else ''}{meta(p)}
    <h2><a href="{url(p)}">{E(p['title'])}</a></h2>
    <p class="post-excerpt">{E(excerpt(p))}</p>
    <p class="card-author">By {E(p['author'])}</p>
    <a class="read-story" href="{url(p)}" aria-label="Read {E(p['title'],quote=True)}">Read the story <span aria-hidden="true">↗</span></a>
  </div>
</article>'''
body='''<section class="blog-intro" aria-labelledby="blog-title"><div class="blog-wrap"><p class="blog-eyebrow">Words from my journey</p><h1 id="blog-title">The blog.</h1><p>Personal reflections on healing, self-trust, relationships, and finding freedom within.</p></div></section>
<section class="blog-collection" aria-label="All blog posts"><div class="blog-wrap">'''+card(POSTS[0],True)+f'<div class="blog-section-label"><h2>All stories</h2><p>{len(POSTS)} posts · 2022–2026</p></div><div class="blog-grid">'+''.join(card(p) for p in POSTS[1:])+'</div></div></section>'
schema={'@context':'https://schema.org','@type':'CollectionPage','name':'Blog | Danielle Ronit','url':BASE+'/blog/','mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'url':BASE+url(p),'name':p['title']} for i,p in enumerate(POSTS)]}}
(ROOT/'blog').mkdir(exist_ok=True)
(ROOT/'blog/index.html').write_text(document('Blog','Personal stories and reflections by Danielle Ronit on healing, relationships, self-trust, and freedom within.','/blog/',body,schema))
for i,p in enumerate(POSTS):
 updated=f'<p class="post-updated">Updated {E(p["displayModified"])}</p>' if p['displayModified']!=p['displayDate'] else ''
 body=f'''<article class="blog-article">
 <header class="article-header"><a class="back-to-blog" href="/blog/">← All stories</a>{meta(p)}<h1>{E(p['title'])}</h1><p class="article-author">By {E(p['author'])}</p>{updated}</header>
 <figure class="article-cover"><img src="{p['image']}" alt="{E(p['imageAlt'],quote=True)}" fetchpriority="high"></figure>
 <div class="article-body">{p['bodyHtml']}</div>
 <div class="article-end"><p>Written by {E(p['author'])}</p></div>
 </article>'''
 related=[q for q in POSTS if q['slug']!=p['slug']][:2]
 body+='<section class="blog-related blog-wrap" aria-labelledby="related-title"><div class="blog-section-label"><h2 id="related-title">Keep reading</h2><a class="back-to-blog" href="/blog/">All stories →</a></div><div class="blog-grid">'+''.join(card(q) for q in related)+'</div></section>'
 schema={'@context':'https://schema.org','@type':'BlogPosting','headline':p['title'],'description':excerpt(p,280),'datePublished':p['firstPublishedDate'],'dateModified':p['lastPublishedDate'],'author':{'@type':'Person','name':p['author'],'url':BASE+'/'},'image':BASE+p['image'],'mainEntityOfPage':BASE+url(p),'inLanguage':'en'}
 dest=ROOT/'post'/p['slug'];dest.mkdir(parents=True,exist_ok=True)
 (dest/'index.html').write_text(document(p['title'],excerpt(p,160),url(p),body,schema,p['image']))
print(f'Built blog index and {len(POSTS)} article pages.')
