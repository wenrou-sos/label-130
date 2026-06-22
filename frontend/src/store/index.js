import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentPet: null,
    currentRecord: null
  },
  mutations: {
    SET_CURRENT_PET(state, pet) {
      state.currentPet = pet
    },
    SET_CURRENT_RECORD(state, record) {
      state.currentRecord = record
    },
    CLEAR_CURRENT_PET(state) {
      state.currentPet = null
    },
    CLEAR_CURRENT_RECORD(state) {
      state.currentRecord = null
    }
  },
  actions: {
    setCurrentPet({ commit }, pet) {
      commit('SET_CURRENT_PET', pet)
    },
    setCurrentRecord({ commit }, record) {
      commit('SET_CURRENT_RECORD', record)
    },
    clearCurrentPet({ commit }) {
      commit('CLEAR_CURRENT_PET')
      commit('CLEAR_CURRENT_RECORD')
    },
    clearCurrentRecord({ commit }) {
      commit('CLEAR_CURRENT_RECORD')
    }
  },
  getters: {
    currentPet: state => state.currentPet,
    currentRecord: state => state.currentRecord
  }
})
