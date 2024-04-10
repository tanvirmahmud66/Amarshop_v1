document.addEventListener('DOMContentLoaded', function() {
    var currentUrl = window.location.pathname;
    console.log(currentUrl)
    var navItems = document.querySelectorAll('.navItem');


    navItems.forEach(function(navItem) {
        var link = navItem.querySelector('a');
        var href = link.getAttribute('href');
        console.log("href",href)
        console.log("current_url",currentUrl.startsWith(href))
        if (currentUrl === href || currentUrl.startsWith(href)) {
            navItem.classList.add('selected');
        }else{
            navItem.classList.remove('selected');
        }
    });
});