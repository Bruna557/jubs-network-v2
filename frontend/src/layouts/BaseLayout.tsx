import { Outlet } from "react-router-dom"

import Navigation from "../components/Navigation/Navigations"

import "./BaseLayout.scss"

const BaseLayout = () => {
  return (
    <>
      <Navigation />
      <div className="content">
        <Outlet />
      </div>
    </>
  )
}

export default BaseLayout
