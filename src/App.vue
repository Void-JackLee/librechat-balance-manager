<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { getJSON, postForm, postJSON } from './util/request.js'

interface User {
  name: string
  email: string
  balance: number
}

const users = reactive<User[]>([])
const all_balance = ref<string>()
const balance_json = ref<string>()
const is_json_dialog_open  = ref<boolean>(false)

const clear_loading = (text = "Loading...") => {
  users.length = 0;
  Object.assign(users, [{
    name: text,
    email: '',
    balance: 0
  }])
}

const list_balances = async () => {
  clear_loading()
  try {
    const data = await getJSON('/api/list-balances')
    Object.assign(users, data.data)
  } catch (error: any) {
    alert('Error fetching balances:' + (error.msg || error))
  }
}

const set_all_balances = async () => {
  if (!all_balance.value) return
  if (isNaN(Number(all_balance.value))) {
    alert('Invalid balance value:' + all_balance.value)
    return
  }
  const confirmation = window.confirm(`Are you sure you want to set all user balances to ${all_balance.value}?`)
  if (!confirmation) return
  try {
    clear_loading("Setting...")
    await postForm('/api/set-all-balances', { balance: all_balance.value })
    list_balances()
  } catch (error: any) {
    alert('Error setting all balances:' + (error.msg || error))
  }
}

const set_balance = async (email: string, balance: number) => {
  if (isNaN(balance)) {
    alert('Invalid balance value:' + balance)
    return
  }
  const confirmation = window.confirm(`Are you sure you want to set balance for ${email} to ${balance}?`)
  if (!confirmation) return
  try {
    clear_loading("Setting...")
    await postForm('/api/set-balance', { email, balance })
    list_balances()
  } catch (error: any) {
    alert('Error setting balance for ' + email + ': ' + (error.msg || error))
  }
}

const open_json_dialog = () => {
  is_json_dialog_open.value = true
  balance_json.value = ""
}

const cancel_json_dialog = () => {
  is_json_dialog_open.value = false
}

const set_balances_from_json = async () => {
  if (!balance_json.value) return
  try {
    const data = JSON.parse(balance_json.value)
    if (!Array.isArray(data)) {
      alert('Invalid JSON format')
      return
    }
    clear_loading("Setting...")
    await postJSON('/api/set-balances-from-json', data)
    list_balances()
  } catch (error: any) {
    alert('Error setting balances from JSON:' + (error.msg || error))
  }
}


onMounted(() => {
  list_balances()
})
</script>

<template>
  <div class="balance-page">
    <div class="toolbar">
      <span>一键设置所有用户金额: </span>
      <input type="number" v-model="all_balance" @keydown.enter="set_all_balances" />
      <button @click="set_all_balances">确定</button>
      <button @click="open_json_dialog">从JSON设置</button>
    </div>
    <div class="toolbar json" v-if="is_json_dialog_open">
      <div><span>从JSON设置: </span></div>
      <div style="height: 10px"></div>
      <div>
        <textarea v-model="balance_json"></textarea>
      </div>
      <div style="margin-top: 10px">
        <button style="margin-right: 10px; background: red" @click="cancel_json_dialog">取消</button>
        <button @click="set_balances_from_json">确定</button>
      </div>
    </div>
    <table class="balance-table">
      <thead>
        <tr>
          <th>User Name</th>
          <th>Email</th>
          <th>Balance</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.email">
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td><input v-model="user.balance" type="number" /></td>
          <td><button @click="set_balance(user.email, user.balance)">Set Balance</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
