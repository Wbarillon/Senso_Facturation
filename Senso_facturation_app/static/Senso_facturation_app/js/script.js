/* Script that provides a pop-up menu for mobile version */

const opener = document.getElementById("menu-burger");
const closer = document.getElementById("menu-burger-retract");
const menu = document.getElementById("mobile-menu");

opener.setAttribute('tabindex', '0');
closer.setAttribute('tabindex', '0');

opener.addEventListener('click', (event) => {
    menu.style.display = "flex";
});
menu.addEventListener('click', (event) => {
    menu.style.display = "none";
})