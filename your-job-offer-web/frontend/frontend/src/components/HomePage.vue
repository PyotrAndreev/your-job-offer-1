<template>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="#">LandingPage</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#features">Features</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#contact">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section text-center">
        <div class="container">
            <h1 class="display-4">Welcome to Our Amazing Service</h1>
            <p class="lead">Your one-stop solution for all your needs. Get started today!</p>
            <a href="#features" class="btn btn-primary btn-lg">Explore Features</a>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features text-center">
        <div class="container">
            <h2 class="mb-5">Our Amazing Features</h2>
            <div class="row">
                <div class="col-md-4">
                    <div class="feature-item">
                        <h3>Feature 1</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-item">
                        <h3>Feature 2</h3>
                        <p>Quisque ac nisi nec metus iaculis suscipit a vel enim.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-item">
                        <h3>Feature 3</h3>
                        <p>Curabitur sit amet felis sed erat vulputate varius.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>


    <!-- Footer -->
    <footer class="footer bg-dark text-white py-5">
        <div class="container">
            <div class="row">
                <!-- Footer Links Section -->
                <div class="col-md-4 mb-4">
                    <h5 class="text-uppercase">Quick Links</h5>
                    <ul class="list-unstyled">
                        <li><a href="#" class="text-white">Home</a></li>
                        <li><a href="#features" class="text-white">Features</a></li>
                        <li><a href="#contact" class="text-white">Contact</a></li>
                        <li><a href="#" class="text-white">About Us</a></li>
                    </ul>
                </div>
                
                <!-- Social Media Links Section -->
                <div class="col-md-4 mb-4">
                    <h5 class="text-uppercase">Follow Us</h5>
                        <ul class="list-unstyled">
                            <li><a href="#" class="text-white me-3" aria-label="Facebook">Facebook<i class="bi bi-facebook"></i></a></li>
                            <li><a href="#" class="text-white me-3" aria-label="Twitter">Twitter<i class="bi bi-twitter"></i></a></li>
                            <li><a href="#" class="text-white me-3" aria-label="Instagram">Instagram<i class="bi bi-instagram"></i></a></li>
                            <li><a href="#" class="text-white me-3" aria-label="LinkedIn">LinkedIn<i class="bi bi-linkedin"></i></a></li>
                        </ul>
                </div>

                <!-- Newsletter Section -->
                <div class="col-md-4 mb-4">
                    <h5 class="text-uppercase">Newsletter</h5>
                    <p>Subscribe to our newsletter for the latest updates and offers!</p>
                    <form>
                        <div class="input-group">
                            <input type="email" class="form-control" placeholder="Enter your email" required>
                            <button class="btn btn-primary" type="submit">Subscribe</button>
                        </div>
                    </form>
                </div>
            </div>

            Footer Bottom Section
            <div class="row mt-4">
                <div class="col-12 text-center">
                    <p>&copy; 2024 MyLandingPage. All rights reserved.</p>
                </div>
            </div>
        </div>
    </footer>

</template>

<script>

</script>

<style scoped>
    body {
        background-color: #f4f4f9;
    }

    .hero-section {
        background-color: #38393a;
        color: white;
        padding: 100px 0;
    }

    .features {
        padding: 60px 0;
        background-color: #ffffff;
    }

    .feature-item {
        text-align: center;
        margin-bottom: 30px;
    }

    .footer {
        background-color: #343a40;
        color: white;
        padding: 20px 0;
        text-align: center;
    }

    .btn-primary {
        background-color: #007bff;
        border-color: #007bff;
    }
</style>