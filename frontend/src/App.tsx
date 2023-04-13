import { BrowserRouter, Routes, Route } from "react-router-dom"

import BaseLayout from "./layouts/BaseLayout"
import Timeline from "./pages/Timeline/Timeline"
import Login from "./pages/Login/Login"

import "../node_modules/bootstrap/dist/css/bootstrap.min.css"
import "./App.scss"

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<BaseLayout />}>
          <Route index element={<Timeline />} />
        </Route>
        <Route path="login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
