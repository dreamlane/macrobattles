using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameSceneMain : MonoBehaviour {

	void Start () {
    Debug.Log("Game Scene started");

    // Start the request to get the map of the world, and everything on it.
    StartCoroutine(MapRequestHandler.getMap(this));
	}

	// Update is called once per frame
	void Update () {

  }
}
