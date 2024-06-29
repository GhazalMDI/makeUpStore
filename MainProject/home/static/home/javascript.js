$('.owl-carousel').owlCarousel({
    loop: false,
    margin: 10,
    rtl:true,
    nav: true,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 3
        },
        1000: {
            items: 5
        }
    }
})


$('.owl-carousel-1').owlCarousel({
    stagePadding: 50,
    loop:false,
    margin:10,
    nav:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:3
        },
        1000:{
            items:5
        }
    }
})