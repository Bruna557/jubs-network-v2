import { useEffect, useState } from "react"
import { useSearchParams, useNavigate } from "react-router-dom"
import { useSelector } from "react-redux"
import { Col } from "react-bootstrap"
import InfiniteScroll from "react-infinite-scroll-component"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faSpinner } from "@fortawesome/free-solid-svg-icons"

import { User } from "../../types"
import UserCard from "../../components/UserCard/UserCard"
import { search } from "../../services/userService"
import { getUser } from "../../store/userSlice"
import "./SearchResult.scss"

const SearchResult = () => {
  const navigate = useNavigate()
  const [users, setUsers] = useState<User[]>([])
  const [searchText, setSearchText] = useState("")
  const [searchParams] = useSearchParams()
  const [currentPage, setCurrentPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)
  const user = useSelector(getUser)

  useEffect(() => {
    setSearchText(searchParams.get("q") || "")
    nextPage()
  }, [searchParams.get("q")])

  const nextPage = () => {
    search(user.username, searchParams.get("q") || "", currentPage)
      .then(result => {
        setUsers(result.result)
        setHasMore(result.has_more)
        setCurrentPage(currentPage + 1)
      })
      .catch(() => {
        navigate("/login")
      })
  }

  return (
    <>
      <h4>Search result: {searchText}</h4>
      <div className="results">
      <InfiniteScroll
        dataLength={users.length}
        next={nextPage}
        hasMore={hasMore}
        loader={<FontAwesomeIcon className="spinner" icon={faSpinner} spin/>}
        scrollableTarget="scrollableDiv"
      >
        {users.map((r: User, i:number) =>
          <Col key={i}>
            <UserCard {...r }/>
          </Col>)}
      </InfiniteScroll>
      </div>
    </>
  )
}

export default SearchResult
