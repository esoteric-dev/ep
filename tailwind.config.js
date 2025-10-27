/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./templates/**/*.html",
        "./static/js/**/*.js",
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    orange: "#f99d27",
                    bg: "#fef6ef",
                    text: "#424242",
                    label: "#757575",
                    link: "#c3824e",
                },
            },
            fontFamily: {
                rubik: ["Rubik", "sans-serif"],
            },
            boxShadow: {
                text: "2px 4px 8px rgba(252,226,206,0.2)",
            },
            borderRadius: {
                arch: "394px",
            },
        },
    },
    plugins: [],
};
