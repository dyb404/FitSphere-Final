# Debug Login Issue

## Steps to Debug:

1. **Open Browser Console** (F12)
2. **Clear localStorage**:
   ```javascript
   localStorage.clear()
   ```
3. **Try to login**
4. **Check console logs** - you should see:
   - "API login response:"
   - "Response data:"
   - "Extracted token:"
   - "Token stored:"

## What to Check:

1. **If "Extracted token: Missing"**:
   - The backend response format might be different
   - Check the Network tab to see the actual response

2. **If "Token stored: No"**:
   - localStorage might be disabled
   - Check browser settings

3. **If token is stored but then disappears**:
   - Something is clearing it
   - Check for other code that calls `localStorage.removeItem('token')`

## Quick Test:

Run this in browser console after login attempt:
```javascript
console.log('Token:', localStorage.getItem('token'))
console.log('User:', localStorage.getItem('user'))
console.log('All keys:', Object.keys(localStorage))
```

