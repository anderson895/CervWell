$(document).ready(function () {
    $("#Get_cervical_recommendation").click(function () {
        let isValid = true;
        let emptyFields = [];

        // Loop through all input fields and validate
        $("input").each(function () {
            if ($(this).val().trim() === "") {
                let fieldName = $(this).attr("id").replace(/-/g, " ").toUpperCase(); // Get the field ID and format it
                emptyFields.push(fieldName);
                isValid = false;
            }
        });

        if (!isValid) {
            alertify.error("Please fill out the following fields: <br>" + emptyFields.join("<br>"));
            return; // Stop execution if validation fails
        }

        let userInput = {
            "Age": Number($("#age").val()),
            "Smokes (years)": Number($("#smoking-years").val()),
            "Smokes (packs/year)": Number($("#packs-per-year").val()),
            "Smokes": Number($("#smokes").val()),
            "Number of sexual partners": Number($("#partners").val()),
            "First sexual intercourse": Number($("#first-intercourse").val()),
            "Number of pregnancies": Number($("#pregnancies").val()),  
            "Hormonal Contraceptives": Number($("#contraceptive-use").val()), 
            "Hormonal Contraceptives (years)": Number($("#contraceptive-duration").val()),
            "IUD": Number($("#iud-use").val()),
            "IUD (years)": Number($("#iud-duration").val()),
            "STDs": Number($("#stds").val()),
            "STDs (number)": Number($("#stds-number").val()),
            "STDs: Number of diagnoses": Number($("#stds-diagnosis-number").val()),  
            "STDs: Time since first diagnosis": Number($("#stds-first-diagnosis").val()),
            "STDs: Time since last diagnosis": Number($("#stds-last-diagnosis").val()),

            "STDs: Condylomatosis": Number($("#stds-condylomatosis").val()),
            "STDs: Cervical Condylomatosis": Number($("#stds-cervical-condylomatosis").val()),
            "STDs: Vaginal Condylomatosis": Number($("#stds-vaginal-condylomatosis").val()),
            "STDs: Vulvo-perineal condylomatosis": 0,  
            "STDs: Syphilis": 0,  
            "STDs: Pelvic inflammatory disease": 0,  
            "STDs: Genital herpes": 0,  
            "STDs: Molluscum contagiosum": 0,  
            "STDs: AIDS": 0,  
            "STDs: HIV": 0,  
            "STDs: Hepatitis B": 0,  
            "STDs: HPV": 0,  

            "Dx:CIN": Number($("#dx-cin").val()),
            "Dx:HPV": Number($("#dx-hpv").val())
        };

        console.log("📤 Sending Data:", userInput); // ✅ Debugging

        $.ajax({
            type: "POST",
            url: "/predict",
            contentType: "application/json",
            data: JSON.stringify(userInput),
            success: function (response) {
                console.log("✅ Response Received:", response);
                $("#recommendation-result").html(`
                    <p><strong>Prediction:</strong> ${response.prediction}</p>
                    <p><strong>Probability:</strong> ${response.probability}%</p>
                `);
            },
            error: function (xhr, status, error) {
                console.error("❌ Error:", xhr.responseText);
                $("#recommendation-result").html(`<p style="color:red;">Error: ${xhr.responseText}</p>`);
            }
        });
    });
});
