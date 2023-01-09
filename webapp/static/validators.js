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

function validateForm(form) {
  let validationResults = [];
  let formElements = [];

  if (form?.ageForm?.value !== undefined) {
    validationResults.push(validateAge(form.ageForm.value));
    formElements.push(form.ageForm);
  }

  if (form?.yearForm?.value !== undefined) {
    validationResults.push(validateYear(form.yearForm.value));
    formElements.push(form.yearForm);
  }

  if (form?.firstNameForm?.value !== undefined) {
    validationResults.push(validateName(form.firstNameForm.value));
    formElements.push(form.firstNameForm);
  }

  if (form?.lastNameForm?.value !== undefined) {
    validationResults.push(validateName(form.lastNameForm.value));
    formElements.push(form.lastNameForm);
  }

  if (form?.countryForm?.value !== undefined) {
    validationResults.push(validateCountry(form.countryForm.value));
    formElements.push(form.countryForm);
  }

  if (form?.sexForm?.value !== undefined) {
    validationResults.push(validateSex(form.sexForm.value));
    formElements.push(form.sexForm);
  }

  if (form?.eraForm?.value !== undefined) {
    validationResults.push(validateEra(form.eraForm.value));
    formElements.push(form.eraForm);
  }

  if (form?.occupationSetForm?.value !== undefined) {
    validationResults.push(validateOccupationSet(form.occupationSetForm.value));
    formElements.push(form.occupationSetForm);
  }

  if (form?.tagsForm?.value !== undefined) {
    validationResults.push(validateTags(form.tagsForm.value));
    formElements.push(form.tagsForm);
  }

  for (let i = 0; i < validationResults.length; i++) {
    if (validationResults[i]) {
      formElements[i].classList.remove("is-invalid");
    } else {
      formElements[i].classList.add("is-invalid");
    }
  }

  // TODO: validate occupation
  // occupationForm
  return validationResults.every((result) => result === true);
}

function validateAge(age) {
  if (age.toLowerCase() === "") {
    return true;
  }
  if (isNaN(Number(age))) {
    return false;
  }
  return Number(age) >= 15 && Number(age) <= 90;
}

function validateName(characterName) {
  return !(characterName.length > 0 && characterName.trim() === "");
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

export { validateForm, eraMap, occupationSetMap };
