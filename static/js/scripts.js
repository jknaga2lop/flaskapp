function confirmDeleteProfile(profileName, profileId) {
    var r = confirm("Are you sure you want to delete the profile: " + profileName + "?");
    if (r == true) {
        window.location.href = '/delete/' + profileId;
    }
}

function navigateToSelectedProfile() {
    const profileId = document.getElementById('profileSelector').value;
    window.location.href = '/edit/' + profileId;
}

function checkProcessAndSetCurrent(selectElement, currentInputName) {
    var currentInput = document.getElementsByName(currentInputName)[0];
    if (selectElement.value === "PAU") {
        currentInput.value = "0";
    }
}