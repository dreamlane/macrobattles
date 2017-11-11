using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameSceneMain : MonoBehaviour {

  public int currentTurn = 0;

  public float timeRemaining = 3;
	// Use this for initialization
	void Start () {
    // Get the map of the world. If no map, then offer a join game button.
    WWWForm form = new WWWForm();
	}

	// Update is called once per frame
	void Update () {
		// Check once per every few second to see if the turn has ended.
    timeRemaining -= Time.deltaTime;
    if (timeRemaining < 0) {
      // Make the request to get some data
      timeRemaining = 200; // long timeout. when the request returns we reset to 3 sec.
    }
	}
}
