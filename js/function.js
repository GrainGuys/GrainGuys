(function ($) {
  "use strict";

  var $window = $(window);
  var $body = $("body");
  var isStaticDemoHost = location.hostname.endsWith(".github.io");

  /* Preloader Effect */
  $window.on("load", function () {
    $(".preloader").fadeOut(600);
  });

  /* Sticky Header */
  if ($(".active-sticky-header").length) {
    $window.on("resize", function () {
      setHeaderHeight();
    });

    function setHeaderHeight() {
      $("header.main-header").css(
        "height",
        $("header .header-sticky").outerHeight()
      );
    }

    $window.on("scroll", function () {
      var fromTop = $(window).scrollTop();
      setHeaderHeight();
      var headerHeight = $("header .header-sticky").outerHeight();
      $("header .header-sticky").toggleClass(
        "hide",
        fromTop > headerHeight + 100
      );
      $("header .header-sticky").toggleClass("active", fromTop > 600);
    });
  }

  /* Slick Menu JS */
  $("#menu").slicknav({
    label: "",
    prependTo: ".responsive-menu",
  });

  if ($("a[href='#top']").length) {
    $(document).on("click", "a[href='#top']", function () {
      $("html, body").animate({ scrollTop: 0 }, "slow");
      return false;
    });
  }

  /* Hero Slider Layout JS */
  const hero_slider_layout = new Swiper(".hero-slider-layout .swiper", {
    effect: "fade",
    slidesPerView: 1,
    speed: 1000,
    spaceBetween: 0,
    loop: true,
    autoplay: {
      delay: 4000,
    },
    pagination: {
      el: ".hero-pagination",
      clickable: true,
    },
  });

  /* testimonial Slider JS */
  var testimonial_slider;

  function initTestimonialClampOnElement($content) {
    var $p = $content.find("p").first();
    if (!$p.length || $content.hasClass("is-expanded")) {
      return;
    }

    $content.removeClass("is-clamped is-expandable");
    $content.removeAttr("role tabindex aria-expanded title");

    $content.addClass("is-clamped");
    if ($p[0].scrollHeight > $p[0].clientHeight + 2) {
      $content.addClass("is-expandable");
      $content.attr({
        role: "button",
        tabindex: "0",
        "aria-expanded": "false",
        title: "Click to read full review",
      });
    } else {
      $content.removeClass("is-clamped");
    }
  }

  function initTestimonialClamp() {
    $(".testimonial-content").each(function () {
      initTestimonialClampOnElement($(this));
    });

    if (testimonial_slider) {
      if (testimonial_slider.updateAutoHeight) {
        testimonial_slider.updateAutoHeight();
      } else if (testimonial_slider.update) {
        testimonial_slider.update();
      }
    }
  }

  function collapseExpandedTestimonials($scope) {
    ($scope || $(".our-testimonials, .page-testimonials"))
      .find(".testimonial-content.is-expanded")
      .each(function () {
        var $content = $(this);
        $content.removeClass("is-expanded").attr("aria-expanded", "false");
        initTestimonialClampOnElement($content);
      });
  }

  if ($(".testimonial-slider").length) {
    testimonial_slider = new Swiper(".testimonial-slider .swiper", {
      slidesPerView: 1,
      speed: 1000,
      spaceBetween: 30,
      loop: true,
      autoHeight: true,
      autoplay: {
        delay: 5000,
      },
      pagination: {
        el: ".testimonial-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: ".testimonial-btn-next",
        prevEl: ".testimonial-btn-prev",
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
        },
        991: {
          slidesPerView: 2,
        },
      },
    });

    testimonial_slider.on("slideChangeTransitionStart", function () {
      collapseExpandedTestimonials($(".our-testimonials"));
    });

    testimonial_slider.on("slideChangeTransitionEnd", function () {
      initTestimonialClamp();
    });
  }

  $(document).on("click", ".testimonial-content.is-expandable", function (e) {
    e.preventDefault();
    var $content = $(this);
    var $scope = $content.closest(".our-testimonials, .page-testimonials");

    if ($content.hasClass("is-expanded")) {
      $content.removeClass("is-expanded").attr("aria-expanded", "false");
      initTestimonialClampOnElement($content);
      if (testimonial_slider) {
        if (testimonial_slider.updateAutoHeight) {
          testimonial_slider.updateAutoHeight();
        } else if (testimonial_slider.update) {
          testimonial_slider.update();
        }
      }
      return;
    }

    $scope.find(".testimonial-content.is-expanded").each(function () {
      var $other = $(this);
      $other.removeClass("is-expanded").attr("aria-expanded", "false");
      initTestimonialClampOnElement($other);
    });

    $content.addClass("is-expanded").removeClass("is-clamped");
    $content.attr("aria-expanded", "true");

    if (testimonial_slider) {
      if (testimonial_slider.updateAutoHeight) {
        testimonial_slider.updateAutoHeight();
      } else if (testimonial_slider.update) {
        testimonial_slider.update();
      }
    }
  });

  $(document).on("keydown", ".testimonial-content.is-expandable", function (e) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      $(this).trigger("click");
    }
  });

  $(window).on("load", function () {
    initTestimonialClamp();
  });

  var testimonialResizeTimer;
  $(window).on("resize", function () {
    clearTimeout(testimonialResizeTimer);
    testimonialResizeTimer = setTimeout(initTestimonialClamp, 200);
  });

  /* Skill Bar */
  if ($(".skills-progress-bar").length) {
    $(".skills-progress-bar").waypoint(
      function () {
        $(".skillbar").each(function () {
          $(this)
            .find(".count-bar")
            .animate(
              {
                width: $(this).attr("data-percent"),
              },
              2000
            );
        });
      },
      {
        offset: "70%",
      }
    );
  }

  /* Init Counter */
  if ($(".counter").length) {
    $(".counter").counterUp({ delay: 6, time: 3000 });
  }

  /* Image Reveal Animation */
  if ($(".reveal").length) {
    gsap.registerPlugin(ScrollTrigger);
    let revealContainers = document.querySelectorAll(".reveal");
    revealContainers.forEach((container) => {
      let image = container.querySelector("img");
      let tl = gsap.timeline({
        scrollTrigger: {
          trigger: container,
          toggleActions: "play none none none",
        },
      });
      tl.set(container, { autoAlpha: 1 });

      tl.from(container, {
        duration: 1,
        xPercent: 100,
        ease: "power2.out",
      });

      tl.from(image, {
        duration: 1,
        xPercent: -100,
        scale: 1,
        delay: -1,
        ease: "power2.out",
      });
    });
  }

  /* Text Effect Animation */
  if ($(".text-anime-style-1").length) {
    let staggerAmount = 0.05,
      translateXValue = 20,
      delayValue = 0.5,
      animatedTextElements = document.querySelectorAll(".text-anime-style-1");

    animatedTextElements.forEach((element) => {
      let animationSplitText = new SplitText(element, { type: "words" });
      gsap.from(animationSplitText.words, {
        duration: 1,
        delay: delayValue,
        x: translateXValue,
        autoAlpha: 0,
        stagger: staggerAmount,
        scrollTrigger: { trigger: element, start: "top 85%" },
      });
    });
  }

  if ($(".text-anime-style-2").length) {
    let staggerAmount = 0.03,
      translateXValue = 20,
      delayValue = 0.1,
      easeType = "power2.out",
      animatedTextElements = document.querySelectorAll(".text-anime-style-2");

    animatedTextElements.forEach((element) => {
      let animationSplitText = new SplitText(element, { type: "words" });
      gsap.from(animationSplitText.words, {
        duration: 1,
        delay: delayValue,
        x: translateXValue,
        autoAlpha: 0,
        stagger: staggerAmount,
        ease: easeType,
        scrollTrigger: { trigger: element, start: "top 85%" },
      });
    });
  }

  if ($(".text-anime-style-3").length) {
    let animatedTextElements = document.querySelectorAll(".text-anime-style-3");

    animatedTextElements.forEach((element) => {
      // Reset if needed
      if (element.animation) {
        element.animation.progress(1).kill();
        element.split.revert();
      }

      element.split = new SplitText(element, {
        type: "lines,words",
        linesClass: "split-line",
      });
      gsap.set(element, { perspective: 400 });

      gsap.set(element.split.words, {
        opacity: 0,
        x: "50",
      });

      element.animation = gsap.to(element.split.words, {
        scrollTrigger: { trigger: element, start: "top 90%" },
        x: "0",
        y: "0",
        rotateX: "0",
        opacity: 1,
        duration: 1,
        ease: "Back.easeOut",
        stagger: 0.02,
      });
    });
  }

  /* Parallaxie js */
  var $parallaxie = $(".parallaxie");
  if ($parallaxie.length && $window.width() > 991) {
    if ($window.width() > 768) {
      $parallaxie.parallaxie({
        speed: 0.55,
        offset: 0,
      });
    }
  }

  /* Zoom Gallery screenshot */
  $(".gallery-items").magnificPopup({
    delegate: "a",
    type: "image",
    closeOnContentClick: false,
    closeBtnInside: false,
    mainClass: "mfp-with-zoom",
    image: {
      verticalFit: true,
    },
    gallery: {
      enabled: true,
    },
    zoom: {
      enabled: true,
      duration: 300, // don't foget to change the duration also in CSS
      opener: function (element) {
        return element.find("img");
      },
    },
  });

  /* Project single page photo viewer dialog */
  function initProjectPhotoViewer() {
    var $container = $(".page-project-single .project-single-content");
    if (!$container.length) {
      return;
    }

    var photos = [];

    $container
      .find(".page-single-image figure, .project-before-after-figure")
      .each(function () {
        var $figure = $(this);
        var $img = $figure.find("img").first();
        if (!$img.length) {
          return;
        }

        var src = $img.attr("src");
        if (!src) {
          return;
        }

        var label = $figure.find(".project-before-after-label").first().text().trim();
        var alt = $img.attr("alt") || "";
        var index = photos.length;

        photos.push({
          src: src,
          alt: alt,
          label: label,
          caption: label ? label + ": " + alt : alt,
        });

        $figure
          .addClass("project-photo-trigger")
          .attr({
            "data-photo-index": index,
            role: "button",
            tabindex: "0",
            "aria-label": "View photo" + (alt ? ": " + alt : ""),
          });
      });

    if (!photos.length) {
      return;
    }

    if (!$("#projectPhotoViewer").length) {
      $("body").append(
        '<div id="projectPhotoViewer" class="project-photo-viewer" hidden aria-hidden="true" role="dialog" aria-modal="true" aria-label="Project photo viewer">' +
          '<div class="project-photo-viewer-backdrop" data-photo-viewer-close></div>' +
          '<div class="project-photo-viewer-dialog">' +
            '<button type="button" class="project-photo-viewer-close" aria-label="Close photo viewer">&times;</button>' +
            '<button type="button" class="project-photo-viewer-nav project-photo-viewer-prev" aria-label="Previous photo">&#10094;</button>' +
            '<button type="button" class="project-photo-viewer-nav project-photo-viewer-next" aria-label="Next photo">&#10095;</button>' +
            '<figure class="project-photo-viewer-figure">' +
              '<img class="project-photo-viewer-image" src="" alt="">' +
              '<figcaption class="project-photo-viewer-caption"></figcaption>' +
            '</figure>' +
            '<p class="project-photo-viewer-counter" aria-live="polite"></p>' +
          "</div>" +
        "</div>"
      );
    }

    var $viewer = $("#projectPhotoViewer");
    var $image = $viewer.find(".project-photo-viewer-image");
    var $caption = $viewer.find(".project-photo-viewer-caption");
    var $counter = $viewer.find(".project-photo-viewer-counter");
    var currentIndex = 0;
    var lastFocus = null;

    function showPhoto(index) {
      currentIndex = index;
      var photo = photos[currentIndex];
      $image.attr({ src: photo.src, alt: photo.alt });
      $caption.text(photo.caption);
      $counter.text(currentIndex + 1 + " / " + photos.length);
      $viewer
        .find(".project-photo-viewer-prev")
        .prop("disabled", currentIndex === 0);
      $viewer
        .find(".project-photo-viewer-next")
        .prop("disabled", currentIndex === photos.length - 1);
    }

    function openViewer(index) {
      lastFocus = document.activeElement;
      showPhoto(index);
      $viewer.removeAttr("hidden").attr("aria-hidden", "false");
      $("body").addClass("project-photo-viewer-open");
      $viewer.find(".project-photo-viewer-close").trigger("focus");
    }

    function closeViewer() {
      $viewer.attr({ hidden: "hidden", "aria-hidden": "true" });
      $("body").removeClass("project-photo-viewer-open");
      $image.attr("src", "");
      if (lastFocus) {
        $(lastFocus).trigger("focus");
      }
    }

    function showRelative(step) {
      var nextIndex = currentIndex + step;
      if (nextIndex >= 0 && nextIndex < photos.length) {
        showPhoto(nextIndex);
      }
    }

    $container.on("click", ".project-photo-trigger", function (event) {
      event.preventDefault();
      openViewer(parseInt($(this).attr("data-photo-index"), 10));
    });

    $container.on("keydown", ".project-photo-trigger", function (event) {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openViewer(parseInt($(this).attr("data-photo-index"), 10));
      }
    });

    $viewer.on("click", "[data-photo-viewer-close], .project-photo-viewer-close", function () {
      closeViewer();
    });

    $viewer.on("click", ".project-photo-viewer-prev", function () {
      showRelative(-1);
    });

    $viewer.on("click", ".project-photo-viewer-next", function () {
      showRelative(1);
    });

    $viewer.on("click", ".project-photo-viewer-dialog", function (event) {
      event.stopPropagation();
    });

    $(document).on("keydown.projectPhotoViewer", function (event) {
      if ($viewer.attr("aria-hidden") === "true") {
        return;
      }

      if (event.key === "Escape") {
        closeViewer();
      } else if (event.key === "ArrowLeft") {
        showRelative(-1);
      } else if (event.key === "ArrowRight") {
        showRelative(1);
      }
    });
  }

  initProjectPhotoViewer();

  /* Contact form validation */
  var $contactform = $("#contactForm");
  $contactform.validator({ focus: false }).on("submit", function (event) {
    if (!event.isDefaultPrevented()) {
      event.preventDefault();
      submitForm();
    }
  });

  function submitForm() {
    if (isStaticDemoHost) {
      formSuccess();
      submitMSG(
        true,
        "Demo site — form not sent. Use a PHP host for live submissions."
      );
      return;
    }

    /* Ajax call to submit form */
    $.ajax({
      type: "POST",
      url: "form-process.php",
      data: $contactform.serialize(),
      success: function (text) {
        if (text === "success") {
          formSuccess();
        } else {
          submitMSG(false, text);
        }
      },
    });
  }

  function formSuccess() {
    $contactform[0].reset();
    submitMSG(true, "Your message was sent successfully!");
  }

  function submitMSG(valid, msg) {
    if (valid) {
      var msgClasses = "h4 text-success";
    } else {
      var msgClasses = "h4 text-danger";
    }
    $("#msgSubmit").removeClass().addClass(msgClasses).text(msg);
  }
  /* Contact form validation end */

  /* Appointment form validation */
  var $requestquoteForm = $("#requestquoteForm");
  $requestquoteForm.validator({ focus: false }).on("submit", function (event) {
    if (!event.isDefaultPrevented()) {
      event.preventDefault();
      submitappointmentForm();
    }
  });

  function submitappointmentForm() {
    if (isStaticDemoHost) {
      appointmentformSuccess();
      appointmentsubmitMSG(
        true,
        "Demo site — form not sent. Use a PHP host for live submissions."
      );
      return;
    }

    /* Ajax call to submit form */
    $.ajax({
      type: "POST",
      url: "form-appointment.php",
      data: $requestquoteForm.serialize(),
      success: function (text) {
        if (text === "success") {
          appointmentformSuccess();
        } else {
          appointmentsubmitMSG(false, text);
        }
      },
    });
  }

  function appointmentformSuccess() {
    $appointmentForm[0].reset();
    appointmentsubmitMSG(true, "Your message was sent successfully!");
  }

  function appointmentsubmitMSG(valid, msg) {
    if (valid) {
      var msgClasses = "h3 text-success";
    } else {
      var msgClasses = "h3 text-danger";
    }
    $("#msgSubmit").removeClass().addClass(msgClasses).text(msg);
  }
  /* Appointment form validation end */

  /* Animated Wow Js */
  new WOW().init();

  /* Service Entry Step Item Active Start */
  var $service_solution_steps = $(".service-solution-steps");
  if ($service_solution_steps.length) {
    var $service_step = $service_solution_steps.find(
      ".service-solution-step-item"
    );

    if ($service_step.length) {
      $service_step.on({
        mouseenter: function () {
          if (!$(this).hasClass("active")) {
            $service_step.removeClass("active");
            $(this).addClass("active");
          }
        },
        mouseleave: function () {
          // Optional: Add logic for mouse leave if needed
        },
      });
    }
  }
  /*Service Entry Step Item Active End  */
})(jQuery);

// jalaliDatepicker removed for English site
