document.addEventListener("DOMContentLoaded", function () {

    document.body.addEventListener("click", function (event) {
        if (event.target.matches("#addEducation")) {
            addEducationEntry();
        } else if (event.target.matches("#addLicense")) {
            addLicenseEntry();
        } else if (event.target.matches("#addWork")) {
            addWorkEntry();
        } else if (event.target.matches(".remove-btn")) {
            let section = event.target.closest(".entry").parentNode;
            event.target.closest(".entry").remove();
            checkEmptySection(section);
        }
    });

    function addEducationEntry() {
        removeNoRecordMessage("#educationSection");
        let educationContainer = document.createElement("div");
        educationContainer.classList.add("row", "g-3", "mt-3", "entry");
        educationContainer.innerHTML = `
            <div class="col-md-3">
                <label class="form-label">School Graduated</label>
                <input type="text" class="form-control school" placeholder="School Graduated" required>
            </div>
            <div class="col-md-3">
                <label class="form-label">Degree/Course</label>
                <input type="text" class="form-control degree" placeholder="Degree/Course" required>
            </div>
            <div class="col-md-3">
                <label class="form-label">Year Graduated</label>
                <select class="form-select yearGraduated">${generateYearOptions()}</select>
            </div>
            <div class="col-md-3 d-flex align-items-end">
                <button type="button" class="btn btn-danger remove-btn">Remove</button>
            </div>
        `;
        document.querySelector("#educationSection").appendChild(educationContainer);
    }

    function addLicenseEntry() {
        removeNoRecordMessage("#licenseSection");
        let licenseContainer = document.createElement("div");
        licenseContainer.classList.add("row", "g-3", "mt-3", "entry");
        licenseContainer.innerHTML = `
            <div class="col-md-3">
                <label class="form-label">License or Certification Name</label>
                <input type="text" class="form-control license" placeholder="License or Certification Name" required>
            </div>
            <div class="col-md-3">
                <label class="form-label">Issuing Organization</label>
                <input type="text" class="form-control org" placeholder="Issuing Organization" required>
            </div>
            <div class="col-md-2">
                <label class="form-label">Issue Date</label>
                <input type="date" class="form-control issueDate" required>
            </div>
            <div class="col-md-2">
                <label class="form-label">Expiration Date</label>
                <input type="date" class="form-control expirationDate" required>
            </div>
            <div class="col-md-2 d-flex align-items-end">
                <button type="button" class="btn btn-danger remove-btn">Remove</button>
            </div>
        `;
        document.querySelector("#licenseSection").appendChild(licenseContainer);
    }

    function addWorkEntry() {
        removeNoRecordMessage("#workSection");
        let workContainer = document.createElement("div");
        workContainer.classList.add("row", "g-3", "mt-3", "entry");
        workContainer.innerHTML = `
            <div class="col-md-3">
                <label class="form-label">Company Name</label>
                <input type="text" class="form-control company" placeholder="Company Name (e.g., Google, Microsoft)" required>
            </div>
            <div class="col-md-3">
                <label class="form-label">Position</label>
                <input type="text" class="form-control position" placeholder="(e.g., Software Engineer)" required>
            </div>
            <div class="col-md-2">
                <label class="form-label">Start Date</label>
                <input type="date" class="form-control startDate">
            </div>
            <div class="col-md-2">
                <label class="form-label">End Date</label>
                <input type="date" class="form-control endDate">
            </div>
            <div class="col-md-1 d-flex align-items-end">
                <button type="button" class="btn btn-danger remove-btn">Remove</button>
            </div>
        `;
        document.querySelector("#workSection").appendChild(workContainer);
    }

    function removeNoRecordMessage(sectionSelector) {
        let section = document.querySelector(sectionSelector);
        let noRecordMessage = section.querySelector(".no-record");
        if (noRecordMessage) {
            noRecordMessage.remove();
        }
    }

    function checkEmptySection(section) {
        if (!section.querySelector(".entry")) {
            let message = document.createElement("p");
            message.classList.add("text-muted", "no-record");

            if (section.id === "educationSection") {
                message.textContent = "No education records found.";
            } else if (section.id === "licenseSection") {
                message.textContent = "No license records found.";
            } else if (section.id === "workSection") {
                message.textContent = "No work experience records found.";
            }

            section.appendChild(message);
        }
    }
});
