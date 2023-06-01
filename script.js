date = new Date();
    year = date.getFullYear();
    window.onload(initials());

    function initials() {
        document.getElementById('age-counter').innerHTML=year - 1999 - 1 + (date.getMonth() >= 11 ? 1 : 0);  //check your birthmonth has passed, if yes you are on years old (mine is dec, so 11, jan is 0) just replace 11 with your birth month(ignore day for now)
        document.getElementById('copyright-year').innerHTML=year;
    }