$(document).ready(function () {
    let page = 1;
    const pageSize = 20;

    function fetchStories(page) {

        let query = $('#search-input').val().trim();

        $('table').hide();
        $('.pagination-controls').hide();

        $('#searching-message').removeClass('d-none').show();

        let url = `/api/filtered-stories/?page=${page}&page_size=${pageSize}`;
        if (query) {
            url += `&q=${encodeURIComponent(query)}`;
        }

        $.ajax({
            url: url,
            type: "GET",
            success: function (response) {
                let storiesTable = $("tbody");
                storiesTable.empty();

                // Hide the searching message
                $('#searching-message').addClass('d-none').hide();

                // Show table and pagination again
                $('table').show();
                $('.pagination-controls').show()

                if (response.results.length === 0) {
                    storiesTable.append('<tr><td colspan="4" class="text-center">No stories found.</td></tr>');
                } else {
                    response.results.forEach(function (stories) {
                        let isActive = stories.is_active ? "active" : "inactive";

                        let truncatedTitle = stories.title.split(" ").slice(0, 5).join(" ");
                        if (stories.title.split(" ").length > 5) {
                            truncatedTitle += "...";
                        }

                        let eventDate = new Date(stories.created_at);
                        let formattedDate = eventDate.toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                        });
                        let formattedTime = eventDate.toLocaleTimeString('en-US', {
                            hour: 'numeric',
                            minute: 'numeric',
                            hour12: true
                        });
                        let formattedDateTime = `${formattedDate}, ${formattedTime}`;

                        let row = `
                        <tr>
                            <td data-label="Event">${stories.title}</td>
                            <td data-label="User">${stories.user_email}</td>
                            <td data-label="Author">${stories.user_is_staff ? 'Staff' : 'Alumni'}</td>
                            <td data-label="Date">${formattedDateTime}</td>
                            <td data-label="Actions" class="action-icons">
                                <a href="/faculty/stories-view/${stories.id}/"><i class="fas fa-eye"></i></a>
                                 ${stories.user_is_staff ? `<a href="/faculty/story-edit/${stories.id}/"><i class="fas fa-edit"></i></a>` : ''}
                                <a href="#" class="delete-item" data-id="${stories.id}" data-type="stories" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>
                            </td>
                            <td class="text-center" data-label="Active">
                                <button class="${isActive === 'active' ? 'unpublish-btn' : 'publish-btn'} toggle-status-btn" data-id="${stories.id}">
                                    ${isActive === 'active' ? 'Unpublish' : 'Publish'}
                                </button>
                            </td>
                        </tr>
                    `;
                        storiesTable.append(row);
                    });
                }
                $('#searching-message').addClass('d-none').hide();
                $('table').show();
                $('.pagination-controls').show();
                createPagination(page, Math.ceil(response.count / pageSize), 5);
            },
            error: function (error) {
                console.error("Error fetching stories:", error);
            }
        });
    }

    // Pagination controls
    $(document).on("click", "#pagination .page-link", function (e) {
        e.preventDefault();
        let newPage = parseInt($(this).data("page"));
        if (!isNaN(newPage)) {
            page = newPage;
            const query = $("#search-input").val();
            fetchStories(page, query);
        }
    });

    // Toggle status publish/unpublish
    $(document).on("click", ".toggle-status-btn", function () {
        const button = $(this);
        const eventId = button.data("id");

        $.ajax({
            url: `/stories/toggle_status/${eventId}/`,
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

                showToast("Success", "Event status updated successfully!", "success");
            },
            error: function (xhr, status, error) {
                console.error("Error toggling event status:", error);
            }
        });
    });

    // Search on button click
    $("#search-button").on("click", function () {
        const query = $("#search-input").val();
        page = 1;
        fetchStories(page, query);
    });

    // Optional: Search on Enter key
    $('#search-input').on('keypress', function (e) {
        if (e.which === 13) { // Enter key
            e.preventDefault();
            page = 1;
            fetchStories(page);
        }
    });

    // Initial fetch
    fetchStories(page);
});
