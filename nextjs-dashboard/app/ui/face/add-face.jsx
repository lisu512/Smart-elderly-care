"use client";

import {Box, TextField} from '@mui/material';
import React, {useState} from 'react';
import axios from "axios";
import ImageUpload from "@/app/ui/image-upload";


export default function AddFace() {
    const [name, setName] = useState('');
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [phone, setPhone] = useState('');
    const handleAddOld = (file) => {
        const data = new FormData();
        data.append('name', name);
        data.append('room', '');
        data.append('age', age);
        data.append('gender', gender);
        data.append('phone', phone);
        data.append("type", "worker")
        data.append('image', file);
        const config = {
            method: 'post',
            url: 'http://127.0.0.1:5000/oldman',
            data: data
        };
        axios(config)
            .then(function (response) {
                console.log(JSON.stringify(response.data));
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    return (
        <Box display="flex" sx={{flexDirection: 'column'}}>
            <TextField
                required
                id="name"
                label="名称"
                value={name}
                sx={{width: 200, m: 1}}
                onChange={(e) => setName(e.target.value)}

            />
            <TextField
                required
                id="age"
                label="年龄"
                type="number"
                value={age}
                sx={{width: 200, m: 1}}
                onChange={(e) => setAge(e.target.value)}
            />
            <TextField
                required
                id="gender"
                label="性别"
                value={gender}
                sx={{width: 200, m: 1}}
                onChange={(e) => setGender(e.target.value)}
            />
            <TextField
                required
                id="phone"
                label="电话"
                value={phone}
                sx={{width: 200, m: 1}}
                onChange={(e) => setPhone(e.target.value)}
            />
            <ImageUpload onUpload={handleAddOld}/>
        </Box>

    );
}