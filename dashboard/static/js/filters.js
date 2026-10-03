const searchInput =
    document.getElementById("projectSearch");

const sectorFilter =
    document.getElementById("sectorFilter");

const riskFilter =
    document.getElementById("riskFilter");


// =========================================
// PROJECT FILTER
// =========================================

function filterProjects() {

    const searchValue =
        searchInput.value.toLowerCase();

    const sectorValue =
        sectorFilter.value.toLowerCase();

    const riskValue =
        riskFilter.value.toLowerCase();


    const rows =
        document.querySelectorAll(
            "#projectRiskTable tbody tr"
        );


    rows.forEach(row => {

        const rowText =
            row.innerText.toLowerCase();


        const sectorMatch =
            !sectorValue ||
            rowText.includes(sectorValue);


        const riskMatch =
            !riskValue ||
            rowText.includes(riskValue);


        const searchMatch =
            !searchValue ||
            rowText.includes(searchValue);


        if (
            sectorMatch &&
            riskMatch &&
            searchMatch
        ) {

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

    });

}


// =========================================
// FILTER EVENTS
// =========================================

searchInput.addEventListener(
    "input",
    filterProjects
);


sectorFilter.addEventListener(
    "change",
    filterProjects
);


riskFilter.addEventListener(
    "change",
    filterProjects
);



// =========================================
// PROJECT DETAILS MODAL
// =========================================

const projectLinks =
    document.querySelectorAll(
        ".project-link"
    );


projectLinks.forEach(link => {

    link.addEventListener(
        "click",
        function(event) {

            event.preventDefault();


            // -----------------------------
            // CURRENT PROJECT ROW
            // -----------------------------

            const row =
                this.closest("tr");


            const cells =
                row.querySelectorAll("td");


            // -----------------------------
            // BASIC PROJECT INFORMATION
            // -----------------------------

            const projectName =
                this.innerText.trim();


            const projectCode =
                this.dataset.project;


            const ministry =
                cells[1].innerText.trim();


            const sector =
                cells[2].innerText.trim();



            // -----------------------------
            // COST / DATE INFORMATION
            // -----------------------------

            const originalCost =
                this.dataset.originalCost;


            const revisedCost =
                this.dataset.revisedCost;


            const expenditure =
                this.dataset.expenditure;


            const originalDate =
                this.dataset.originalDate;


            const revisedDate =
                this.dataset.revisedDate;



            // -----------------------------
            // RISK INFORMATION
            // -----------------------------

            const riskScore =
                cells[7].innerText.trim();


            const riskLevel =
                cells[8].innerText.trim();


            const costRisk =
                cells[9].innerText.trim();


            const timeRisk =
                cells[10].innerText.trim();


            const warning =
                cells[11].innerText.trim();



            // =================================
            // SEND BASIC DATA TO MODAL
            // =================================

            document.getElementById(
                "modalProjectName"
            ).innerText =
                projectName;


            document.getElementById(
                "modalProjectCode"
            ).innerText =
                "Project Code: " +
                projectCode;


            document.getElementById(
                "modalMinistry"
            ).innerText =
                ministry;


            document.getElementById(
                "modalSector"
            ).innerText =
                sector;



            // =================================
            // COST INFORMATION
            // =================================

            document.getElementById(
                "modalOriginalCost"
            ).innerText =
                originalCost || "N/A";


            document.getElementById(
                "modalRevisedCost"
            ).innerText =
                revisedCost || "N/A";


            document.getElementById(
                "modalExpenditure"
            ).innerText =
                expenditure || "N/A";



            // =================================
            // DATE INFORMATION
            // =================================

            document.getElementById(
                "modalOriginalDate"
            ).innerText =
                originalDate ||
                "Not available";


            document.getElementById(
                "modalRevisedDate"
            ).innerText =
                revisedDate ||
                "Not available";



            // =================================
            // RISK INFORMATION
            // =================================

            document.getElementById(
                "modalRiskScore"
            ).innerText =
                riskScore;


            document.getElementById(
                "modalRiskLevel"
            ).innerText =
                riskLevel;


            document.getElementById(
                "modalCostRisk"
            ).innerText =
                costRisk;


            document.getElementById(
                "modalTimeRisk"
            ).innerText =
                timeRisk;


            document.getElementById(
                "modalWarning"
            ).innerText =
                warning;



            // =================================
            // COST CHANGE CALCULATION
            // =================================

            const originalCostValue =
                parseFloat(originalCost);


            const revisedCostValue =
                parseFloat(revisedCost);


            let costChange =
                "N/A";


            if (
                originalCostValue > 0 &&
                !isNaN(revisedCostValue)
            ) {

                costChange =
                    (
                        (
                            (
                                revisedCostValue -
                                originalCostValue
                            )
                            /
                            originalCostValue
                        )
                        *
                        100
                    ).toFixed(1);

            }


            document.getElementById(
                "modalCostChange"
            ).innerText =
                costChange;



            // =================================
            // SCHEDULE DELAY CALCULATION
            // =================================

            const originalDateValue =
                new Date(originalDate);


            const revisedDateValue =
                new Date(revisedDate);


            let delayDays =
                "N/A";


            if (
                !isNaN(originalDateValue) &&
                !isNaN(revisedDateValue)
            ) {

                delayDays =
                    Math.round(
                        (
                            revisedDateValue -
                            originalDateValue
                        )
                        /
                        (
                            1000 *
                            60 *
                            60 *
                            24
                        )
                    );

            }


            document.getElementById(
                "modalDelayDays"
            ).innerText =
                delayDays;



            // =================================
            // OPEN MODAL
            // =================================

            document.getElementById(
                "projectModal"
            ).classList.add(
                "show"
            );

        }
    );

});



// =========================================
// CLOSE PROJECT MODAL
// =========================================

document.addEventListener(
    "DOMContentLoaded",
    function() {


        const modal =
            document.getElementById(
                "projectModal"
            );


        const closeButton =
            document.getElementById(
                "closeProjectModal"
            );


        if (
            !modal ||
            !closeButton
        ) {

            return;

        }



        // -----------------------------
        // CLOSE BUTTON
        // -----------------------------

        closeButton.addEventListener(
            "click",
            function() {

                modal.classList.remove(
                    "show"
                );

            }
        );



        // -----------------------------
        // CLOSE WHEN CLICKING OUTSIDE
        // -----------------------------

        modal.addEventListener(
            "click",
            function(event) {

                if (
                    event.target === modal
                ) {

                    modal.classList.remove(
                        "show"
                    );

                }

            }
        );

    }
);