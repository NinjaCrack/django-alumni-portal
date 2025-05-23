$(document).ready(function () {
    let page = 1;
    const pageSize = 20;


    function fetchCareers(page) {
        $.ajax({
            url: `/api/filtered-jobposts/?page=${page}&page_size=${pageSize}`,
            type: "GET",
            success: function (response) {
                let careersTable = $("tbody");
                careersTable.empty();

                response.results.forEach(function (careers) {
                    let isActive = careers.is_active ? "active" : "inactive";

                    let truncatedTitle = careers.title.split(" ").slice(0, 5).join(" ");
                    if (careers.title.split(" ").length > 5) {
                        truncatedTitle += "...";
                    }

                    let row = `
                        <tr>
                            <td data-label="Title">${truncatedTitle}</td>
                            <td data-label="Company">${careers.company}</td>
                            <td data-label="Location">${careers.location}</td>
                            <td data-label="Job Type">${careers.job_type}</td>
                            <td data-label="Actions" class="action-icons text-nowrap">
                                <a href="/faculty/careers-view/${careers.id}"><i class="fas fa-eye"></i></a>
                                <a href="/faculty/careers-edit/${careers.id}"><i class="fas fa-edit"></i></a>
                                <a href="#" class="delete-item" data-id="${careers.id}" data-type="career" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>
                            </td>
                            <td class="text-center" data-label="Active">
                                <button class="${isActive === 'active' ? 'unpublish-btn' : 'publish-btn'} toggle-status-btn" data-id="${careers.id}">
                                    ${isActive === 'active' ? 'Unpublish' : 'Publish'}
                                </button>
                            </td>
                        </tr>
                    `;
                    careersTable.append(row);
                });

                createPagination(page, Math.ceil(response.count / pageSize), 5);
            },
            error: function (xhr, status, error) {
                console.error("Error fetching alumni:", error);
            }
        });
    }

    // Function to create pagination
    $(document).on("click", "#pagination .page-link", function (e) {
        e.preventDefault();
        let newPage = parseInt($(this).data("page"));
        if (!isNaN(newPage)) {
            page = newPage;
            fetchCareers(page);
        }
    });

    // Handle publish/unpublish button click
    $(document).on("click", ".toggle-status-btn", function () {
        const button = $(this);
        const jobId = button.data("id");

        $.ajax({
            url: `/careers/toggle_status/${jobId}/`,
            type: "POST",
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function () {
                if (button.hasClass("publish-btn")) {
                    button.removeClass("publish-btn").addClass("unpublish-btn").text("Unpublish");
                } else {
                    button.removeClass("unpublish-btn").addClass("publish-btn").text("Publish");
                }

                showToast("Success", "Job status updated successfully!", "success");
            },
            error: function (xhr, status, error) {
                console.error("Error toggling job status:", error);
            }
        });
    });

    fetchCareers(page);
});