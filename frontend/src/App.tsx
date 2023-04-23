import { BrowserRouter, Routes, Route , Navigate} from "react-router-dom"

import BaseLayout from "./layouts/BaseLayout"
import Timeline from "./pages/Timeline/Timeline"
import SearchResult from "./pages/SearchResult/SearchResult"
import Followers from "./pages/Followers/Followers"
import Following from "./pages/Following/Following"
import Login from "./pages/Login/Login"
import Register from "./pages/Register/Register"

import "../node_modules/bootstrap/dist/css/bootstrap.min.css"
import "./App.scss"

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<BaseLayout />}>
          <Route path="home" element={<Timeline />} />
          <Route path="search" element={<SearchResult />} />
          <Route path="followers" element={<Followers />} />
          <Route path="following" element={<Following />} />
        </Route>
        <Route path="/" element={<Navigate to="/login"/>} />
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
