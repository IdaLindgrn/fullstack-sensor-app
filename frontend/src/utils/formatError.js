export const validateForm = (fields, type = 'login') => {
  const { email = '', username = '', password = '' } = fields;
  const errors = [];

  if (!email.trim()) errors.push('Email is required.');
  else if (!email.includes('@')) errors.push('Email must include @.');

  if (type === 'register') {
    if (!username.trim()) errors.push('Username is required.');
    else if (username.length < 3)
      errors.push('Username must be at least 3 characters.');
    else if (username.length > 50)
      errors.push('Username cannot exceed 50 characters.');
  }

  if (type === 'register') {
    if (!password.trim()) errors.push('Password is required.');
    else if (password.length < 6)
      errors.push('Password must be at least 6 characters.');
  }

  if (type === 'login' && !password.trim())
    errors.push('Password is required.');

  return errors;
};
