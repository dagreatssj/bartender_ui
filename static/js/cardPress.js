let cardDiv = document.querySelectorAll('.card');
let editButtonDiv = document.querySelectorAll('.edit-button');

for (let j = 0; j < editButtonDiv.length; j++) {
  editButtonDiv[j].addEventListener('click', function(e) {
    let drinkId = this.dataset.drinkId;
    window.location.href = "/edit/" + drinkId;
    e.stopPropagation();
  });
}


for (let i = 0; i < cardDiv.length; i++) {
  cardDiv[i].addEventListener('click', function() {
    var drinkName = this.getElementsByClassName('card-title')[0].innerHTML;
    console.log(drinkName);
  });
}
