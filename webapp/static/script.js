"use strict";
// Cards and buttons
const characterCard = document.getElementById("character-card");
const generateButtons = document.getElementsByClassName("btn-primary");
const warningAlert = document.getElementById("warning-alert");
const resetButton = document.getElementById("reset-btn");

// Character card elements
const characterName = document.getElementById("character-name");
const characterInfo = document.getElementById("character-info");
const strength = document.getElementById("str");
const condition = document.getElementById("con");
const size = document.getElementById("siz");
const dexterity = document.getElementById("dex");
const appearance = document.getElementById("app");
const education = document.getElementById("edu");
const intelligence = document.getElementById("int");
const power = document.getElementById("pow");
const luck = document.getElementById("luck");
const damageBonus = document.getElementById("damage-bonus");
const build = document.getElementById("build");
const doge = document.getElementById("doge");
const moveRate = document.getElementById("move-rate");
const skills = document.getElementById("skills");
const hitPoints = document.getElementById("hit-points");
const magicPoints = document.getElementById("magic-points");

// Form elements
const firstNameForm = document.getElementById("validation-first-name");
const lastNameForm = document.getElementById("validation-last-name");
const countryForm = document.getElementById("validation-country");
const ageForm = document.getElementById("validation-age");
const yearForm = document.getElementById("validation-year");
const sexForm = document.getElementById("validation-sex");
const occupationForm = document.getElementById("validation-occupation");

// Advanced form elements
const eraForm = document.getElementById("validation-era");
const occupationSetForm = document.getElementById("validation-occupation-set");
const tagsForm = document.getElementById("validation-tags");

// Cochar variables
const availableCountries = new Set(["US", "PL", "ES"]);
const availableSex = new Set(["Male", "Female", "Random"]);
const availableEra = new Set(["classic-1920", "modern", "classic-1920,modern"]);
const availableOccupationSet = new Set([
  "classic",
  "expansion",
  "custom",
  null,
]);
const availableTags = new Set(["lovecraftian", "criminal", null]);

const countriesMap = new Map([
  ["(US) United States", "US"],
  ["(PL) Poland", "PL"],
  ["(ES) Spain", "ES"],
]);

const eraMap = new Map([
  ["Modern", "modern"],
  ["Classic 1920", "classic-1920"],
  ["All", "classic-1920,modern"],
]);

const occupationSetMap = new Map([
  ["Keeper Rulebook", "classic"],
  ["Investigators Handbook", "expansion"],
  ["Custom", "custom"],
  ["All", null],
]);

// Main Functions
function loadingSpinnerOn() {
  for (let button of generateButtons) {
    button.setAttribute("disabled", "");
    button.innerHTML =
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
  }
}

function loadingSpinnerOff() {
  for (let button of generateButtons) {
    button.removeAttribute("disabled");
    button.innerHTML = "Generate Character";
  }
}

function sendRequest(
  firstName = "",
  lastName = "",
  country = "",
  age = "",
  sex = "",
  year = "",
  random_mode = "",
  occupation = "",
  era = "",
  occupationSet = "",
  tags = ""
) {
  // const url = new URL("http://0.0.0.0:80/api/get");
  const url = new URL("http://127.0.0.1:5000/api/get");
  // const url = new URL("https://cochar.loca.lt/api/get");

  if (firstName) url.searchParams.append("first_name", firstName);
  if (lastName) url.searchParams.append("last_name", lastName);
  if (age) url.searchParams.append("age", age);
  if (year) url.searchParams.append("year", year);
  if (country) url.searchParams.append("country", country);
  if (sex) url.searchParams.append("sex", sex);
  if (random_mode) url.searchParams.append("random_mode", random_mode);
  if (occupation) url.searchParams.append("occupation", occupation);
  if (occupationSet) url.searchParams.append("occup_type", occupationSet);
  if (era) url.searchParams.append("era", era);
  if (tags) url.searchParams.append("tags", tags);

  console.log(url);
  fetch(url)
    .then((response) => {
      if (!response.ok)
        throw new Error(`${response.status}, ${response.statusText}`);
      return response.json();
    })
    .then((data) => {
      console.log(data);
      // Here add message about fails
      if (data?.status === "fail") {
        warningAlert.classList.remove("hidden");
        warningAlert.innerText = data?.message;
        throw new Error(data.message);
      }
      warningAlert.classList.add("hidden");
      updateForm(data);
    })
    .catch((e) => console.error(e))
    .finally(loadingSpinnerOff);
}

// TODO: Data validation

function updateForm(data) {
  // Show Character card
  characterCard.classList.remove("hidden");

  // Render text
  characterName.textContent = `${data.sex === "M" ? "Mr." : "Ms."} ${
    data.first_name
  } ${data.last_name}`;
  characterInfo.textContent = `${data.age} yo, ${data.occupation}, ${data.country}`;

  strength.innerHTML = `<strong>STR:</strong> ${data.strength}`;
  condition.innerHTML = `<strong>CON:</strong> ${data.condition}`;
  size.innerHTML = `<strong>SIZ:</strong> ${data.size}`;
  dexterity.innerHTML = `<strong>DEX:</strong> ${data.dexterity}`;
  appearance.innerHTML = `<strong>APP:</strong> ${data.appearance}`;
  education.innerHTML = `<strong>EDU:</strong> ${data.education}`;
  intelligence.innerHTML = `<strong>INT:</strong> ${data.intelligence}`;
  power.innerHTML = `<strong>POW:</strong> ${data.power}`;
  luck.innerHTML = `<strong>Luck</strong>: ${data.luck}`;
  damageBonus.innerHTML = `<strong>Damage bonus:</strong> ${data.damage_bonus}`;
  build.innerHTML = `<strong>Build:</strong> ${data.build}`;
  doge.innerHTML = `<strong>Doge:</strong> ${data.doge}`;
  moveRate.innerHTML = `<strong>Move rate:</strong> ${data.move_rate}`;
  hitPoints.innerHTML = `<strong>Hit points:</strong> ${data.hit_points}`;
  magicPoints.innerHTML = `<strong>Magic points:</strong> ${data.magic_points}`;

  // skills.innerHTML = ""
  let temp_skills = [];
  for (const [skill_name, skill_value] of Object.entries(data.skills)) {
    // temp_skills.push(`<strong>${skill_name.replace(skill_name[0], skill_name[0].toUpperCase())}:</strong> ${skill_value}%`)
    temp_skills.push(
      `<div class="col-lg-6 col-md-12 col-sm-12"><strong>${skill_name.replace(
        skill_name[0],
        skill_name[0].toUpperCase()
      )}</strong> ${skill_value}%</div>`
    );
  }
  // skills.textContent = temp_skills.join(", ")
  // skills.insertAdjacentElement("beforeend", temp_skills.join(""))
  temp_skills.sort();
  skills.innerHTML = temp_skills.join("");
}

function validateForm() {
  if (!validateAge(ageForm.value)) {
    ageForm.classList.add("is-invalid");
    return false;
  } else {
    ageForm.classList.remove("is-invalid");
  }

  if (!validateYear(yearForm.value)) {
    yearForm.classList.add("is-invalid");
    return false;
  } else {
    yearForm.classList.remove("is-invalid");
  }

  if (!validateName(firstNameForm.value)) {
    firstNameForm.classList.add("is-invalid");
    return false;
  } else {
    firstNameForm.classList.remove("is-invalid");
  }

  if (!validateName(lastNameForm.value)) {
    lastNameForm.classList.add("is-invalid");
    return false;
  } else {
    lastNameForm.classList.remove("is-invalid");
  }

  if (!validateCountry(countryForm.value)) {
    countryForm.classList.add("is-invalid");
    return false;
  } else {
    countryForm.classList.remove("is-invalid");
  }

  if (!validateSex(sexForm.value)) {
    sexForm.classList.add("is-invalid");
    return false;
  } else {
    sexForm.classList.remove("is-invalid");
  }

  if (!validateEra(eraForm.value)) {
    eraForm.classList.add("is-invalid");
    return false;
  } else {
    eraForm.classList.remove("is-invalid");
  }

  if (!validateOccupationSet(occupationSetForm.value)) {
    occupationSetForm.classList.add("is-invalid");
    return false;
  } else {
    occupationSetForm.classList.remove("is-invalid");
  }

  if (!validateTags(tagsForm.value)) {
    tagsForm.classList.add("is-invalid");
    return false;
  } else {
    tagsForm.classList.remove("is-invalid");
  }

  // TODO: validate occupation
  // occupationForm
  return true;
}

function validateAge(age) {
  if (age.toLowerCase() === "") {
    return true;
  }
  return Number(age) >= 15 && Number(age) <= 90;
}

function validateName(characterName) {
  return !(characterName === " " || characterName[0] === " ");
}

function validateCountry(country) {
  // TODO: create available country list based on backend
  const alpha2code = countriesMap.get(country);
  return availableCountries.has(alpha2code);
}

function validateYear(year) {
  if (isNaN(year)) {
    return false;
  }
  return typeof Number(year) === "number";
}

function validateSex(sex) {
  return availableSex.has(sex);
}

function validateEra(era) {
  const eraCode = eraMap.get(era);
  return availableEra.has(eraCode);
}

function validateOccupationSet(occupationSet) {
  return true;
}

function validateTags(tags) {
  if (!tags) return true;

  const givenTags = tags.split(",");
  for (let tag of givenTags) {
    console.log(tag);
    if (!availableTags.has(tag)) return false;
  }

  return true;
}

function generateCharacter() {
  if (!validateForm()) {
    return false;
  }

  loadingSpinnerOn();

  let firstName = firstNameForm.value;
  let lastName = lastNameForm.value;
  let country = countriesMap.get(countryForm.value);
  let age = ageForm.value;
  let sex = sexForm.value.toLowerCase();
  let year = yearForm.value;
  let occupation = occupationForm.value.toLowerCase();
  let random_mode;
  let era = eraMap.get(eraForm.value);
  let occupationSet = occupationSetMap.get(occupationSetForm.value);
  let tags = tagsForm.value;

  if (sex === "random") sex = "";
  if (sex === "male") sex = "M";
  if (sex === "female") sex = "F";
  if (occupation.split(" ")[0] === "random") {
    random_mode = true;
    occupation = "";
  }
  if (occupation.split(" ")[0] === "optimal") occupation = "";

  if (validateForm()) {
    sendRequest(
      firstName,
      lastName,
      country,
      age,
      sex,
      year,
      random_mode,
      occupation,
      era,
      occupationSet,
      tags
    );
  }
}

document.getElementById("validation-country").value = "(US) United States";

function resetForm() {
  // Form elements
  firstNameForm.value = "";
  lastNameForm.value = "";
  countryForm.value = "(US) United States";
  ageForm.value = "";
  yearForm.value = 1925;
  sexForm.value = "Random";
  occupationForm.value = "optimal (max skill points)";

  // Advanced form elements
  eraForm.value = "Classic 1920";
  occupationSetForm.value = "Keeper Rulebook";
  tagsForm.value = "";
}

for (let button of generateButtons) {
  button.addEventListener("click", generateCharacter);
}

resetButton.addEventListener("click", resetForm);

// Generate character when page is loaded
generateCharacter();

// TODO: Disable form submission with invalid data
// TODO: Sort occupation
