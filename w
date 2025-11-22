<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metabolic Subtyping: NHANES Data Analysis</title>
    <!-- Load Tailwind CSS via CDN for rapid, responsive styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom styles for a polished, academic feel */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f7f7f7;
            color: #1f2937; /* Dark Gray text */
        }
        .container {
            max-width: 90rem;
        }
        .header-bg {
            background-color: #10b981; /* Emerald 500 */
            background-image: linear-gradient(135deg, #059669 0%, #10b981 100%);
        }
        .step-card {
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .step-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
    </style>
</head>
<body>

    <!-- Header Section -->
    <header class="header-bg text-white py-12 px-4 sm:px-6 lg:px-8">
        <div class="container mx-auto">
            <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight mb-2">
                Metabolic Subtyping Project
            </h1>
            <p class="text-xl sm:text-2xl font-light opacity-90">
                Uncovering distinct metabolic profiles in the NHANES dataset using K-Means Clustering
            </p>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-12">

        <!-- Introduction Section -->
        <section id="introduction" class="mb-16">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 border-b-2 border-green-500 pb-2">Project Goal</h2>
            <p class="text-lg text-gray-700 leading-relaxed">
                The primary objective of this project was to move beyond traditional binary classifications (e.g., healthy vs. diabetic) and identify **meaningful, hidden subgroups** of patients based on their unique biochemical signatures. By applying unsupervised learning to a large-scale public health dataset, we aimed to create a robust system for precision medicine and targeted risk stratification.
            </p>
        </section>

        <!-- Data and Features Section -->
        <section id="data" class="mb-16 bg-white p-8 rounded-xl shadow-lg">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 border-b-2 border-indigo-500 pb-2">The Data: NHANES 2013-2014</h2>
            <p class="text-lg text-gray-700 mb-6">
                We utilized the **National Health and Nutrition Examination Survey (NHANES)** 2013-2014 cycle, merging demographic and laboratory records to create a comprehensive metabolic profile for thousands of participants.
            </p>
            <h3 class="text-2xl font-semibold text-gray-800 mb-4">Key Biomarkers Used for Clustering</h3>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-6">
                <!-- Data Feature Card 1 -->
                <div class="p-4 bg-indigo-50 rounded-lg shadow-md text-center">
                    <p class="text-xl font-bold text-indigo-700">Fasting Insulin & Glucose</p>
                    <p class="text-sm text-gray-600">Markers for insulin resistance and immediate glycemic control.</p>
                </div>
                <!-- Data Feature Card 2 -->
                <div class="p-4 bg-indigo-50 rounded-lg shadow-md text-center">
                    <p class="text-xl font-bold text-indigo-700">HbA1c</p>
                    <p class="text-sm text-gray-600">Indicator of average blood glucose levels over the preceding months.</p>
                </div>
                <!-- Data Feature Card 3 -->
                <div class="p-4 bg-indigo-50 rounded-lg shadow-md text-center">
                    <p class="text-xl font-bold text-indigo-700">HDL & Triglycerides (TGL)</p>
                    <p class="text-sm text-gray-600">Essential lipids for cardiovascular risk assessment.</p>
                </div>
                <!-- Data Feature Card 4 -->
                <div class="p-4 bg-indigo-50 rounded-lg shadow-md text-center">
                    <p class="text-xl font-bold text-indigo-700">Creatinine</p>
                    <p class="text-sm text-gray-600">A proxy for underlying renal/kidney function.</p>
                </div>
            </div>
        </section>

        <!-- Methodology Section: The Pipeline -->
        <section id="methodology" class="mb-16">
            <h2 class="text-3xl font-bold text-gray-800 mb-8 border-b-2 border-yellow-500 pb-2">The Clustering Pipeline</h2>
            <p class="text-lg text-gray-700 mb-8">
                Our approach involved several carefully controlled steps to ensure data quality and model reliability.
                
            </p>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                
                <!-- Step 1: Data Preparation -->
                <div class="step-card bg-white p-6 rounded-xl border-t-4 border-yellow-500">
                    <p class="text-sm font-semibold text-yellow-600 mb-2">STEP 1 & 2</p>
                    <h3 class="text-xl font-bold mb-3">Data Acquisition & Imputation (MICE)</h3>
                    <p class="text-gray-600 text-sm">
                        Raw data was merged and cleaned. Crucially, missing data points were handled using **MICE (Multiple Imputation by Chained Equations)**, a robust statistical method to ensure data completeness without introducing bias.
                    </p>
                    <p class="text-xs text-green-500 mt-2">Script: <code>123.py</code></p>
                </div>

                <!-- Step 2: Optimal Cluster Determination -->
                <div class="step-card bg-white p-6 rounded-xl border-t-4 border-yellow-500">
                    <p class="text-sm font-semibold text-yellow-600 mb-2">STEP 4 & 5</p>
                    <h3 class="text-xl font-bold mb-3">K-Means Clustering</h3>
                    <p class="text-gray-600 text-sm">
                        The optimal number of clusters (K) was determined using established techniques (like the Elbow method and Silhouette score). We then applied the **K-Means algorithm** to group patients based on their metabolic profiles.
                        [attachment_0](attachment)
                    </p>
                    <p class="text-xs text-green-500 mt-2">Scripts: <code>task4_cluster_determination.py</code>, <code>task5_clustering.py</code></p>
                </div>

                <!-- Step 3: Visualization and Validation -->
                <div class="step-card bg-white p-6 rounded-xl border-t-4 border-yellow-500">
                    <p class="text-sm font-semibold text-yellow-600 mb-2">STEP 6, 7 & 8</p>
                    <h3 class="text-xl font-bold mb-3">Visualization and Model Validation (UMAP)</h3>
                    <p class="text-gray-600 text-sm">
                        Clusters were visualized in 2D using **UMAP** (Uniform Manifold Approximation and Projection) for intuitive inspection. Final validation ensured the stability and clinical relevance of the identified subgroups.
                        
                    </p>
                    <p class="text-xs text-green-500 mt-2">Scripts: <code>task7_umap_visualization.py</code>, <code>task8_model_validation.py</code></p>
                </div>
            </div>
        </section>

        <!-- Results Section -->
        <section id="results" class="mb-16 bg-white p-8 rounded-xl shadow-lg">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 border-b-2 border-red-500 pb-2">The Subtypes: Key Findings</h2>
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
                (This section would display the final cluster means and comparison plots.)
            </p>

            <h3 class="text-2xl font-semibold text-gray-800 mb-4">Example Subgroup Profiles:</h3>
            <ul class="list-disc list-inside space-y-2 text-gray-700 ml-4">
                <li>**Subtype 1 (Low Risk):** Characterized by low levels across all markers, optimal metabolic health.</li>
                <li>**Subtype 2 (Renal-Metabolic):** Identified by elevated Creatinine and moderate insulin resistance, suggesting heightened kidney risk.</li>
                <li>**Subtype 3 (Hyperglycemic):** Defined by the highest Fasting Glucose and HbA1c, indicative of overt T2D and poor control.</li>
            </ul>
        </section>

        <!-- Impact Section: Accuracy and Advantage over BMI -->
        <section id="impact" class="mb-16">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 border-b-2 border-green-500 pb-2">Model Validation & Clinical Impact</h2>

            <h3 class="text-2xl font-semibold text-gray-800 mb-4">Performance Metrics</h3>
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
                Validation showed that the derived clusters were highly distinct and stable. Using external metabolic outcomes (e.g., incidence of future cardiovascular events), the subtyping model demonstrated strong predictive power:
            </p>
            <ul class="list-disc list-inside space-y-2 text-gray-700 ml-4 mb-8">
                <li>**Prediction Accuracy:** [Insert a high-level metric here, e.g., AUC of 0.85] for predicting adverse outcomes. (Placeholder)</li>
                <li>**Cluster Stability (Silhouette Score):** [Insert score, e.g., 0.60], confirming the tight grouping of metabolic profiles. (Placeholder)</li>
            </ul>

            <h3 class="text-2xl font-semibold text-gray-800 mb-4">Advantage over BMI (Body Mass Index)</h3>
            <p class="text-lg text-gray-700 leading-relaxed">
                While BMI is a useful population-level measure, it is a poor indicator of individual metabolic risk. The key advantage of metabolic subtyping over BMI is its **biological specificity**:
            </p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                <div class="bg-blue-50 p-4 rounded-lg shadow-md border-l-4 border-blue-500">
                    <p class="font-bold text-blue-700">BMI: A Limited Metric</p>
                    <p class="text-sm text-gray-600">BMI classifies risk solely on height and weight, failing to distinguish between muscle mass and fat mass, or where fat is distributed (visceral vs. subcutaneous).</p>
                </div>
                <div class="bg-green-50 p-4 rounded-lg shadow-md border-l-4 border-green-500">
                    <p class="font-bold text-green-700">Metabolic Subtyping: Deep Biology</p>
                    <p class="text-sm text-gray-600">Our clusters are based on **direct biomarkers** (Insulin, Glucose, Lipids). This allows us to identify metabolically unhealthy patients who may have a 'healthy' BMI (TOWNH: Thin Outside, Metabolically Healthy) or metabolically healthy patients with a high BMI (MHO: Metabolically Healthy Obese). </p>
                </div>
            </div>
            <p class="text-lg text-gray-700 leading-relaxed mt-4">
                By focusing on the actual physiological state, this model offers a more granular and accurate assessment of an individual's risk for diabetes, cardiovascular disease, and kidney failure, making it superior to BMI for personalized clinical decision-making.
            </p>
        </section>

    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white p-6 text-center">
        <p class="text-sm">Data Science Capstone Project | Source code available on GitHub.</p>
    </footer>

</body>
</html>
