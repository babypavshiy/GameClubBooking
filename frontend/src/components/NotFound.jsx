import { Button, Result } from 'antd';
import React from 'react';
import { useNavigate } from'react-router-dom';
const NotFound = () => {
    const navigate  =  useNavigate();
    return (
  <Result
    status="404"
    title="404"
    subTitle="Sorry, the page you visited does not exist."
    extra={<Button type="primary" onClick={() => navigate('/reservations')}>Вернуться на главную</Button>}
  />
);}
export default NotFound;