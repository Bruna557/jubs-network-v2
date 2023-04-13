import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import type { RootState } from "./store"

import { User } from "../types"

interface UserState {
    user: User
}

const initialState: UserState = {
    user: {
        username: "",
        bio: "",
        picture: "",
        isLoggedIn: false
    }
}

/*
 * A "slice" is a collection of Redux reducer logic and actions for a single
 * feature in your app. The name comes from splitting up the root Redux state
 * object into multiple "slices" of state
 *
 * Redux Toolkit allows us to write "mutating" logic in reducers. It
 * doesn't actually mutate the state because it uses the Immer library,
 * which detects changes to a "draft state" and produces a brand new
 * immutable state based off those changes.
*/
export const userSlice = createSlice({
    name: "user",
    initialState,
    reducers: {
        setUser: (state:UserState, action: PayloadAction<User>) => {
            state.user = action.payload
        },
        setIsLoggedIn: (state: UserState, action: PayloadAction<boolean>) => {
            state.user.isLoggedIn = action.payload
        }
    },
})

// Actions
export const { setIsLoggedIn } = userSlice.actions
export const { setUser } = userSlice.actions

// Selectors
export const getUser = (state: RootState) => state.user.user
export const getIsLoggedIn = (state: RootState) => state.user.user.isLoggedIn

// Reducer
export default userSlice.reducer
