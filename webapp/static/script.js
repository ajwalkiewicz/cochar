'use strict'

// Cards and buttons
const characterCard = document.getElementById("character-card")
const generateButton = document.getElementById("generate-btn")

// Character card elements
const characterName = document.getElementById("character-name")
const strength = document.getElementById("str")
const condition = document.getElementById("con")
const size = document.getElementById("siz")
const dexterity = document.getElementById("dex")
const appearance = document.getElementById("app")
const education = document.getElementById("edu")
const intelligence = document.getElementById("int")
const power = document.getElementById("pow")
const luck = document.getElementById("luck")
const damageBonus = document.getElementById("damage-bonus")
const build = document.getElementById("build")
const doge = document.getElementById("doge")
const moveRate = document.getElementById("move-rate")
const skills = document.getElementById("skills") 
const hitPoints = document.getElementById("hit-points") 
const magicPoints = document.getElementById("magic-points") 

// Form elements
const firstNameForm = document.getElementById("validation-first-name") 
const lastNameForm = document.getElementById("validation-last-name") 
const countryForm = document.getElementById("validation-country") 
const ageForm = document.getElementById("validation-age") 
const yearForm = document.getElementById("validation-year") 
const sexForm = document.getElementById("validation-sex") 
const occupationForm = document.getElementById("validation-occupation") 


generateButton.addEventListener("click", generateCharacter)

function sendRequest(firstName = "", lastName = "", country = "", age = "", sex = "", year = "", occupation = ""){
  let url = new URL("http://127.0.0.1:5000/api/get")

  if (firstName) url.searchParams.append("first_name", firstName)  
  if (lastName) url.searchParams.append("last_name", lastName)
  if (age) url.searchParams.append("age", age)
  if (year) url.searchParams.append("year", year)
  if (country) url.searchParams.append("country", country)
  if (sex) url.searchParams.append("sex", sex)
  if (occupation) url.searchParams.append("occupation", occupation)


  fetch(url)
  .then(response => {
    if(!response.ok) throw new Error(`Too many tries: ${response.status}`)
    return response.json()
  })
  .then(data => {
    console.log(data);
    updateForm(data)
  })
}

// TODO: Data validation

function updateForm(data){
  // Show Character card
  characterCard.classList.remove("hidden")
  
  // Render text
  characterName.textContent = `${data.sex === "M" ? "Mr." : "Ms."} ${data.first_name} ${data.last_name}, ${data.age} years old ${data.occupation}, ${data.country}`

  strength.textContent = `STR: ${data.strength}`
  condition.textContent = `CON: ${data.condition}`
  size.textContent = `SIZ: ${data.size}`
  dexterity.textContent = `DEX: ${data.dexterity}`
  appearance.textContent = `APP: ${data.appearance}`
  education.textContent = `EDU: ${data.education}`
  intelligence.textContent = `INT: ${data.intelligence}`
  power.textContent = `POW: ${data.power}`
  luck.textContent = `Luck: ${data.luck}`
  damageBonus.textContent = `Damage bonus: ${data.damage_bonus}`
  build.textContent = `Build: ${data.build}`
  doge.textContent = `Doge: ${data.doge}`
  moveRate.textContent = `Move rate: ${data.move_rate}`
  hitPoints.textContent = `Hit points: ${data.hit_points}`
  magicPoints.textContent = `Magic points: ${data.magic_points}`

  skills.textContent = ""
  let temp_skills = []
  for (const [skill_name, skill_value] of Object.entries(data.skills)){
    temp_skills.push(`${skill_name.replace(skill_name[0], skill_name[0].toUpperCase())}: ${skill_value}`)
  }
  skills.textContent = temp_skills.join(", ")
}

function validateForm(){

  if (!validateAge(ageForm.value)){
    ageForm.classList.add("is-invalid")
    return false
  } else {
    ageForm.classList.remove("is-invalid")
  }

  if (!validateName(firstNameForm.value)){
    firstNameForm.classList.add("is-invalid")
    return false
  } else {
    firstNameForm.classList.remove("is-invalid")
  }

  if (!validateName(lastNameForm.value)){
    lastNameForm.classList.add("is-invalid")
    return false
  } else {
    lastNameForm.classList.remove("is-invalid")
  }

  if (!validateCountry(countryForm.value)){
    countryForm.classList.add("is-invalid")
    return false
  } else {
    countryForm.classList.remove("is-invalid")
  }

  if (!validateYear(yearForm.value)){
    yearForm.classList.add("is-invalid")
    return false
  } else {
    yearForm.classList.remove("is-invalid")
  }
 
  // TODO: validate occupation
  // occupationForm
  return true
}

function validateAge(age){
  if (age.toLowerCase()  === "" ){
    return true
  }
  if (Number(age) >= 15 && Number(age) <= 90){
    return true
  }
  return false
}

function validateName(characterName){
  if (characterName === " "){
    return false
  }
  if (characterName[0] === " "){
    return false
  }
  return true
}

function validateCountry(country){
  // TODO: create available country list based on backend 
  const availableCountries = ["US", "PL", "ES"]
  return availableCountries.includes(country)
}

function validateYear(year){
  if (isNaN(year)){
    return false
  }
  return typeof Number(year) === "number"
}

function validateSex(sex){
  const availableSex = ["M", "F", "Random"]
  return availableSex.includes(sex)
}

function generateCharacter(){
  if (!validateForm){
    return false
  }

  let firstName = firstNameForm.value
  let lastName = lastNameForm.value
  let country = countryForm.value.toUpperCase()
  let age = ageForm.value
  let sex = sexForm.value.toLowerCase()
  let year = yearForm.value
  let occupation = occupationForm.value.toLowerCase()

  if (sex === "random") sex = ""
  if (sex === "male") sex = "M"
  if (sex === "female") sex = "F"

  if (validateForm()){
    sendRequest(
      firstName,
      lastName,
      country,
      age,
      sex,
      year,
      occupation
    )
  }
}

// Generate character when page is loaded
generateCharacter()

// TODO: Disable form submission with invalid data
