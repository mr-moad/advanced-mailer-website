const closeModal = (e) => {
    e.style.display = 'none';
    e.querySelector('.modal-actions .close').removeEventListener('click', closeModal);
    e.querySelector('.fa-circle-xmark').removeEventListener('click', closeModal);
}
const showModal = (e,userEmail) => {
    const modalElement = document.getElementById(e.target.dataset.target);
    modalElement.querySelector('.action-btn').dataset.email = userEmail;
    modalElement.style.display = 'grid';
    if(modalElement.querySelector('.content-text')){
        modalElement.querySelector('.content-text').innerText = `"${userEmail}"`;
    }
    modalElement.querySelector('.modal-actions .close').addEventListener('click', closeModal.bind(null, modalElement), false);
    modalElement.querySelector('.fa-circle-xmark').addEventListener('click', closeModal.bind(null, modalElement), false);
}
const getActionsData = (elementId) => {
    const modalElement = document.getElementById(elementId);
    const userEmail = modalElement.querySelector('.action-btn').dataset.email;
    return userEmail
}
const suspendUser = () => {
    const userEmail = getActionsData("suspendModal");
    location.href = '/admin/suspend/'+ userEmail;
}

const deleteUser = () => {
    const userEmail = getActionsData("deleteModal");
    location.href = '/admin/delete/'+ userEmail;
}

const upgradeUser = () => {
    const userEmail = getActionsData("upgradeModal");
    location.href = '/admin/upgrade/'+ userEmail;
}
const downgradeUser = () => {
    const userEmail = getActionsData("downgradeModal");
    location.href = '/admin/downgrade/'+ userEmail;
}
const reactivateUser = () => {
    const userEmail = getActionsData("reactivateModal");
    location.href = '/admin/reactivate/'+ userEmail;
}
const addLicence = () => {
    const userEmail = getActionsData("adddLicencesModal");
    const numberOfLicences = document.getElementById("numberOfLicences").value;
    if (parseInt(numberOfLicences) > 0){
        location.href = `/admin/add_licence/${userEmail}/${numberOfLicences}`;
    }else{
        alert("number should be bigger than 0")
    }
}

const hideFlash = (e) => {
  e.target.style.display = 'none';
}