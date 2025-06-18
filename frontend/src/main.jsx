import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router";
import { ForecastProvider } from "./contexts/ForecastContext";
import DailyPage from "./pages/DailyPage";
import GeneralPage from "./pages/GeneralPage";
import DynamicsPage from "./pages/DynamicsPage";
import MainLayout from "./layouts/MainLayout";
import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { path: ":city", element: <GeneralPage /> },
      { path: ":city/:date", element: <DailyPage /> },
      { path: ":city/dynamics", element: <DynamicsPage /> },
    ],
  },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router}/>
  </StrictMode>
);
