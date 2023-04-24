import { useState, useEffect } from "react"
import { Outlet, useNavigate } from "react-router-dom"
import { useDispatch, useSelector } from "react-redux"
import { Row, Col } from "react-bootstrap"

import Navigation from "../components/Navigation/Navigations"
import UserCard from "../components/UserCard/UserCard"
import { fetchUser } from "../services/userService"
import { fetchRecommendation } from "../services/userService"
import { User } from "../types"
import { getUser, setUser } from "../store/userSlice"

import "./BaseLayout.scss"

const BaseLayout = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const user = useSelector(getUser)
  const [recommendation, setRecommendation] = useState<User[]>([])

  const isMobile = window.innerWidth <= 770

  useEffect(() => {
    fetchUser(user.username)
      .then(result => {
        dispatch(setUser(result))
      })
      .catch(() => {
        navigate("/login")
      })

    fetchRecommendation(user.username)
      .then(result => {
        setRecommendation(result.result)
      })
      .catch(() => {
        navigate("/login")
      })
  }, [])

  return (
    <>
      <Navigation {...user}/>
      <Row className="content" id="scrollableDiv">
        {!isMobile && <Col className="left-panel" md="3">
          <UserCard {...user}/>
          <p className="people-text">People you may know</p>
          {recommendation?.map((r: User, i: number) =>
            <Col key={i}>
              <UserCard {...r }/>
            </Col>)}
        </Col>}
        <Col className="outlet" md="6">
          <Outlet/>
        </Col>
        {!isMobile && <Col className="right-panel" md="3">
          <img className="ad" src="/assets/ad.png" alt="ad"/>
        </Col>}
      </Row>
    </>
  )
}

export default BaseLayout
