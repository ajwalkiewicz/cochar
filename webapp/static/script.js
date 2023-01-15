// Cochar - create a random character for Call of Cthulhu RPG 7th ed.
// Copyright (C) 2023  Adam Walkiewicz

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.

// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.
import { validateForm, eraMap, occupationSetMap } from "./validators.js";
// Cards and buttons
// const characterCard = document.getElementById("character-card");
const generateBasicButton = document.getElementById("generate-basic-btn");
const generateAdvancedButton = document.getElementById("generate-advanced-btn");
const warningAlert = document.getElementById("warning-alert");
const errorAlert = document.getElementById("error-alert");
const resetButton = document.getElementById("reset-btn");
const saveButton = document.getElementById("save-btn");

// Character card elements
const characterCard = {
  characterName: document.getElementById("character-name"),
  characterInfo: document.getElementById("character-info"),
  strength: document.getElementById("str"),
  condition: document.getElementById("con"),
  size: document.getElementById("siz"),
  dexterity: document.getElementById("dex"),
  appearance: document.getElementById("app"),
  education: document.getElementById("edu"),
  intelligence: document.getElementById("int"),
  power: document.getElementById("pow"),
  luck: document.getElementById("luck"),
  damageBonus: document.getElementById("damage-bonus"),
  build: document.getElementById("build"),
  doge: document.getElementById("doge"),
  moveRate: document.getElementById("move-rate"),
  skills: document.getElementById("skills"),
  hitPoints: document.getElementById("hit-points"),
  magicPoints: document.getElementById("magic-points"),
};

// Advanced Form
const advancedForm = {
  HTMLElement: document.getElementById("form-advanced"),
  firstNameForm: document.getElementById("validation-first-name"),
  lastNameForm: document.getElementById("validation-last-name"),
  countryForm: document.getElementById("validation-country"),
  ageForm: document.getElementById("validation-age"),
  yearForm: document.getElementById("validation-year"),
  sexForm: document.getElementById("validation-sex"),
  occupationForm: document.getElementById("validation-occupation"),
  tagsForm: document.getElementById("validation-tags"),
  eraForm: document.getElementById("validation-era-advanced"),
  occupationSetForm: document.getElementById(
    "validation-occupation-set-advanced"
  ),
};

// Basic Form
const basicForm = {
  HTMLElement: document.getElementById("form-basic"),
  eraForm: document.getElementById("validation-era"),
  occupationSetForm: document.getElementById("validation-occupation-set"),
};

function delay(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

// Main Functions
function loadingSpinnerOn() {
  for (let button of [generateBasicButton, generateAdvancedButton]) {
    button.setAttribute("disabled", "");
    button.innerHTML =
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
  }
}

function loadingSpinnerOff() {
  for (let button of [generateBasicButton, generateAdvancedButton]) {
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
  const currentURL = new URL(window.location.href);
  const url = new URL(`${currentURL.origin}/api/v1/get`);

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
      if (response.status === 400 || response.status === 429) {
        return response.json();
      }
      if (!response.ok)
        throw new Error(`${response.status}, ${response.statusText}`);
      return response.json();
    })
    .then((data) => {
      console.log(data);
      // Here add message about fails
      if (data?.origin === "flask_limiter") {
        errorAlert.classList.remove("hidden");
        errorAlert.innerText = data?.message;
        throw new Error(data.message);
      }
      if (data?.origin === "cochar") {
        warningAlert.classList.remove("hidden");
        warningAlert.innerText = data?.message;
        throw new Error(data.message);
      }
      if (data?.message) {
        warningAlert.classList.remove("hidden");
        warningAlert.innerText = Object.values(data?.message);
        throw new Error(data.message);
      }
      warningAlert.classList.add("hidden");
      updateCharacterCard(data);
    })
    .catch((e) => {
      console.error(e);
    })
    .finally(delay(250).then(loadingSpinnerOff));
}

// TODO: Data validation

function updateCharacterCard(data) {
  // Show Character card
  // characterCard.classList.remove("hidden");

  // Render text
  characterCard.characterName.textContent = `${
    data.sex === "M" ? "Mr." : "Ms."
  } ${data.first_name} ${data.last_name}`;
  characterCard.characterInfo.textContent = `${data.age} yo, ${data.occupation}, ${data.country}`;

  characterCard.strength.innerHTML = `<strong>STR:</strong> ${data.strength}`;
  characterCard.condition.innerHTML = `<strong>CON:</strong> ${data.condition}`;
  characterCard.size.innerHTML = `<strong>SIZ:</strong> ${data.size}`;
  characterCard.dexterity.innerHTML = `<strong>DEX:</strong> ${data.dexterity}`;
  characterCard.appearance.innerHTML = `<strong>APP:</strong> ${data.appearance}`;
  characterCard.education.innerHTML = `<strong>EDU:</strong> ${data.education}`;
  characterCard.intelligence.innerHTML = `<strong>INT:</strong> ${data.intelligence}`;
  characterCard.power.innerHTML = `<strong>POW:</strong> ${data.power}`;
  characterCard.luck.innerHTML = `<strong>Luck</strong>: ${data.luck}`;
  characterCard.damageBonus.innerHTML = `<strong>Damage bonus:</strong> ${data.damage_bonus}`;
  characterCard.build.innerHTML = `<strong>Build:</strong> ${data.build}`;
  characterCard.doge.innerHTML = `<strong>Doge:</strong> ${data.doge}`;
  characterCard.moveRate.innerHTML = `<strong>Move rate:</strong> ${data.move_rate}`;
  characterCard.hitPoints.innerHTML = `<strong>Hit points:</strong> ${data.hit_points}`;
  characterCard.magicPoints.innerHTML = `<strong>Magic points:</strong> ${data.magic_points}`;

  // skills.innerHTML = ""
  let temp_skills = [];
  for (const [skill_name, skill_value] of Object.entries(data.skills)) {
    temp_skills.push(
      `<li><strong>${skill_name.replace(
        skill_name[0],
        skill_name[0].toUpperCase()
      )}</strong> ${skill_value}%</li>`
    );
  }

  // skills.textContent = temp_skills.join(", ")
  // skills.insertAdjacentElement("beforeend", temp_skills.join(""))
  temp_skills.sort();
  characterCard.skills.innerHTML = temp_skills.join("");
}

function generateCharacter(form) {
  if (!validateForm(form)) {
    errorAlert.classList.remove("hidden");
    errorAlert.innerText =
      "Check the form. Some of the fields are filled incorrectly";
    return false;
  } else {
    errorAlert.classList.add("hidden");
  }

  loadingSpinnerOn();

  let firstName = form?.firstNameForm?.value ?? "";
  let lastName = form?.lastNameForm?.value ?? "";
  let country = form?.countriesMap?.get(countryForm.value);
  let age = form?.ageForm?.value;
  let sex = form?.sexForm?.value.toLowerCase();
  let year = form?.yearForm?.value;
  let occupation = form?.occupationForm?.value?.toLowerCase() ?? "";
  let random_mode;
  let era = eraMap.get(form?.eraForm?.value) ?? "";
  let occupationSet =
    occupationSetMap.get(form?.occupationSetForm?.value) ?? "";
  let tags = form?.tagsForm?.value;

  if (sex === "random") sex = "";
  if (sex === "male") sex = "M";
  if (sex === "female") sex = "F";
  if (occupation.split(" ")[0] === "random") {
    random_mode = true;
    occupation = "";
  }
  if (occupation.split(" ")[0] === "optimal") occupation = "";

  if (validateForm(form)) {
    sendRequest(
      firstName.trim(),
      lastName.trim(),
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

function resetForm(form) {
  form.HTMLElement.reset();
  for (const value of Object.values(form)) {
    value.classList.remove("is-invalid");
  }
  errorAlert.classList.add("hidden");
  warningAlert.classList.add("hidden");
}

generateBasicButton.addEventListener("click", () =>
  generateCharacter(basicForm)
);
generateAdvancedButton.addEventListener("click", () =>
  generateCharacter(advancedForm)
);
resetButton.addEventListener("click", () => resetForm(advancedForm));

document.getElementById("validation-country").value = "(US) United States";
// Generate character when page is loaded
generateCharacter();

// TODO: Disable form submission with invalid data
