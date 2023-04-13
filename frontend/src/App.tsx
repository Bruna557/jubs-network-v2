import { BrowserRouter, Routes, Route } from "react-router-dom"

import BaseLayout from "./layouts/BaseLayout"
import Timeline from "./pages/Timeline/Timeline"
import SearchResult from "./pages/SearchResult/SearchResult"
import Login from "./pages/Login/Login"
import Register from "./pages/Register/Register"

import "../node_modules/bootstrap/dist/css/bootstrap.min.css"
import "./App.scss"

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<BaseLayout />}>
          <Route index element={<Timeline />} />
          <Route path="search" element={<SearchResult />} />
        </Route>
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
