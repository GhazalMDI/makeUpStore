$('.owl-carousel').owlCarousel({
    loop:false,
    rtl:true,
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



 const indicator = document.getElementsByClassName('indicator')
        const main = document.querySelector('.main')
        for (let i = 0; i < indicator.length; i++) {
            indicator[i].onclick = (e) => {
                for (let a = 0; a < indicator.length; a++) {
                    indicator[i].classList.remove('active')
                }
                indicator[i].classList.add('active')
                main.src = e.target.src;
            }
        }