# aclue-dart-data-store

## Start
cd src
uvicorn main:app --reload --host=0.0.0.0 --port=6666


example request bodies:
{
    "id": "example-1",
    "creationDate": "2020-07-10 15:00:00.000",
    "throws": [
        {
            "id": 0,
            "scoreString": "d11",
            "imageResolution": { "x": 1, "y": 1},
            "imageLabel": {
                "planeCoordinates": [],
                "dartCoordinates": []
            },
            "imageString": "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
        },
        {
            "id": 1,
            "scoreString": "20",
            "imageResolution": { "x": 2, "y": 2},
            "imageLabel": {
                "planeCoordinates": [],
                "dartCoordinates": []
            },
            "imageString": "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
        },
        {
            "id": 2,
            "scoreString": "1",
            "imageResolution": { "x": 3, "y": 3},
            "imageLabel": {
                "planeCoordinates": [],
                "dartCoordinates": []
            },
            "imageString": "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
        }
    ]
}