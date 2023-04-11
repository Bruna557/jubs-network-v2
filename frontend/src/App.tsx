import { BrowserRouter, Routes, Route } from "react-router-dom"

import BaseLayout from "./layouts/BaseLayout"
import Timeline from "./pages/Timeline/Timeline"

import "../node_modules/bootstrap/dist/css/bootstrap.min.css"
import "./App.scss"

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<BaseLayout />}>
        <Route index element={<Timeline />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
