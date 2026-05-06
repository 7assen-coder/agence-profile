document.addEventListener("DOMContentLoaded", function () {
  /* ── Aperçu bus ──────────────────────────────────── */

  var selBus = document.getElementById("id_bus");
  var busPreview = document.getElementById("busPreview");
  var busLabel = document.getElementById("busLabel");
  var busPlaces = document.getElementById("busPlaces");

  selBus.addEventListener("change", function () {
    var opt = this.options[this.selectedIndex];
    if (this.value && opt.dataset.label) {
      busLabel.textContent = opt.dataset.label;
      busPlaces.textContent = opt.dataset.places;
      busPreview.classList.add("visible");
    } else {
      busPreview.classList.remove("visible");
    }
  });

  /* ── Visualisation route ─────────────────────────── */

  var selDep = document.getElementById("id_ville_depart");
  var selArr = document.getElementById("id_ville_arrivee");
  var cityDep = document.getElementById("cityDep");
  var cityArr = document.getElementById("cityArr");

  function updateRoute() {
    var dep = selDep.options[selDep.selectedIndex];
    var arr = selArr.options[selArr.selectedIndex];
    cityDep.textContent = dep.value ? dep.text : "—";
    cityArr.textContent = arr.value ? arr.text : "—";
  }

  selDep.addEventListener("change", updateRoute);
  selArr.addEventListener("change", updateRoute);

  /* ── Période ─────────────────────────────────────── */

  var periodeInput = document.getElementById("periode");
  var btnMatin = document.getElementById("btn-matin");
  var btnAprem = document.getElementById("btn-aprem");

  function selectPeriode(value) {
    periodeInput.value = value;
    btnMatin.classList.toggle("active", value === "matin");
    btnAprem.classList.toggle("active", value === "apres-midi");
  }

  btnMatin.addEventListener("click", function () {
    selectPeriode("matin");
  });

  btnAprem.addEventListener("click", function () {
    selectPeriode("apres-midi");
  });

  /* ── Validation à la soumission ──────────────────── */

  var form = document.getElementById("trajetForm");

  form.addEventListener("submit", function (e) {
    if (!periodeInput.value) {
      e.preventDefault();
      alert("Veuillez sélectionner une période (matin ou après-midi).");
      return;
    }

    var dep = selDep.value;
    var arr = selArr.value;
    if (dep && arr && dep === arr) {
      e.preventDefault();
      alert(
        "La ville de départ et la ville d'arrivée ne peuvent pas être identiques.",
      );
    }
  });
});
