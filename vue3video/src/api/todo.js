import api from './index.js';

export const getTodo = async (id) => {
    const response = await api.get('todos/' + id);
    return response.data;
}