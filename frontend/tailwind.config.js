const { nextui } = require("@nextui-org/react");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",

    // Or if using `src` directory:
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  darkMode: "class",
  plugins: [
    nextui({
      themes: {
        // Custom Light Theme
        "my-light": {
          extend: "light", // inherit default light values
          colors: {
            background: "#ffffff",
            foreground: "#1a1a1a",
            primary: {
              50: "#E8EAF6",
              100: "#C5CAE9",
              200: "#9FA8DA",
              300: "#7986CB",
              400: "#5C6BC0",
              500: "#3F51B5",
              600: "#3949AB",
              700: "#303F9F",
              800: "#283593",
              900: "#1A237E",
              DEFAULT: "#2c3e50", // Use a dark blue/gray for primary if desired
              foreground: "#ffffff",
            },
            focus: "#5C6BC0",
          },
          layout: {
            disabledOpacity: "0.3",
            radius: {
              small: "4px",
              medium: "6px",
              large: "8px",
            },
            borderWidth: {
              small: "1px",
              medium: "2px",
              large: "3px",
            },
          },
        },
        // Custom Dark Theme (dark gray, similar to Discord/Steam)
        "my-dark": {
          extend: "dark", // inherit default dark values
          colors: {
            background: "#36393F", // Discord-like dark gray
            foreground: "#DCDDDE",
            primary: {
              50: "#4A4D52",
              100: "#43464A",
              200: "#3A3D42",
              300: "#31363A",
              400: "#292E32",
              500: "#202225", // Dark gray primary
              600: "#1D1F23",
              700: "#191B1F",
              800: "#141618",
              900: "#101214",
              DEFAULT: "#202225",
              foreground: "#ffffff",
            },
            focus: "#5865F2",
          },
          layout: {
            disabledOpacity: "0.3",
            radius: {
              small: "4px",
              medium: "6px",
              large: "8px",
            },
            borderWidth: {
              small: "1px",
              medium: "2px",
              large: "3px",
            },
          },
        },
      },
    }),
  ],
};