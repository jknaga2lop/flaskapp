function confirmDelete(profileName, profileId) {
    var r = confirm("Are you sure you want to delete the profile: " + profileName + "?");
    if (r == true) {
        window.location.href = '/delete/' + profileId;
    }
}