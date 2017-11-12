using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameSceneMain : MonoBehaviour {
  public GameObject mapObject;
  public MapEngine mapEngine;

	void Start () {
    Debug.Log("Game Scene started");
    // Get a handle on the mapObject, and its script.
    mapObject = GameObject.FindWithTag("Map");
    mapEngine = mapObject.GetComponent(typeof(MapEngine)) as MapEngine;

    // Start the request to get the map of the world.
    StartCoroutine(MapRequestHandler.getMap(this));
	}

	// Update is called once per frame
	void Update () {
    // Build the MapTile game objects if the map hasn't been built yet.
    if (!mapEngine.isMapBuilt()) {
      Debug.Log("Map not built.");
    }
	}
}
