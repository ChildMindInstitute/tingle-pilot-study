# matter-website
Child Minds MATTER website: [matter.childmind.org](http://matter.childmind.org)

### Front Page
In posts, set the optional `frontpage` parameter to `true` for that post to appear 
in its respective category on the front page.

### Projects
Project posts are in '/_posts' with categories.
Images are in '/assets/img/projects'.

### People
People are in '/_people' with categories [team, advisors,...].
Images are in '/assets/img/people/'.

### Blog
Read time is calculated the same way as [*Medium* does](https://help.medium.com/hc/en-us/articles/214991667-Read-time):

> At the top of each Medium story, you'll see an estimated read time.
>
> Read time is based on the average reading speed of an adult (roughly 265 WPM). We take the total word count of a post and translate it into minutes, with an adjustment made for images. For posts in Chinese, Japanese and Korean, it's a function of number of characters (500 characters/min) with an adjustment made for images.

Unlike *Medium*, we currently do not adjust for images.

An optional `excluded-words` parameter in the yaml at the top of a blog post takes an integer to subtract from the word count, eg, words in a References section.

### Images
All images are 300 ppi resolution.
Project images are 600 x 450 (width x height, in pixels); thumbnails are 400 x 300.
People images are 400 x 400 and thumbnails are 225 x 225.
Slideshow images are 1170 x 450 (short) and 700 x 525 (tall) 
and are in '/assets/img/slideshow/'.

### Background
Based on the Agency Jekyll theme, which is in turn based on the
[Agency bootstrap theme](https://startbootstrap.com/template-overviews/agency/)
(see [documentation](http://jekyllrb.com/)).

Instructions for building and running Jekyll locally (bundle exec jekyll serve):
https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/

