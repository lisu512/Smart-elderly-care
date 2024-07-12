import React, {useState} from 'react';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import {styled} from "@mui/material";
import Box from "@mui/material/Box";
import Avatar from "@mui/material/Avatar";
import axios from 'axios';

export default function ImageUpload({onUpload}) {
    const placeholderImage = "/img.png"; // 替换为你的占位图片URL
    const [image, setImage] = useState(placeholderImage);
    const [selectedFile, setSelectedFile] = useState(null);
    const uploadImage = async () => {
        onUpload(selectedFile);
    };
    const handleImageChange = (e) => {
        setImage(URL.createObjectURL(e.target.files[0]));
        setSelectedFile(e.target.files[0]);
    };
    const VisuallyHiddenInput = styled('input')({
        clip: 'rect(0 0 0 0)',
        clipPath: 'inset(50%)',
        height: 1,
        overflow: 'hidden',
        position: 'absolute',
        bottom: 0,
        left: 0,
        whiteSpace: 'nowrap',
        width: 1,
    });
    return (
        <Box display="flex" sx={{flexDirection: 'column', width: 200}}>
            <Box>
                {image && <Avatar alt="Preview" src={image} sx={{width: 200, height: 200}}/>}
            </Box>
            <Button
                size="medium"
                component="label"
                role={undefined}
                variant="contained"
                tabIndex={-1}
                startIcon={<CloudUploadIcon/>}
            >
                添加人脸照片
                <VisuallyHiddenInput type="file" onChange={handleImageChange}/>
            </Button>
            <Button
                sx={{mt: 2, width: 200}}
                variant="contained"
                color="primary" onClick={uploadImage}>
                上传信息
            </Button>

        </Box>
    );
}