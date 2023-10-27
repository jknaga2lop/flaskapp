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