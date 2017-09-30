/**
 * Created by doraoline on 24.12.16.
 */

function read(btn) {
    console.log("Pushing read-button")
    glyph = btn.children[0];

    /* If not read */
    if (glyph.classList.contains("glyphicon-minus")) {
        glyph.classList.remove("glyphicon-minus");
        glyph.classList.add("glyphicon-ok");
        console.log("Read)");
        btn.children[1].innerHTML = "Lest";
        btn.value = "Lest";
    }
    /* If read */
    else if (glyph.classList.contains("glyphicon-ok")) {
        glyph.classList.remove("glyphicon-ok");
        glyph.classList.add("glyphicon-minus");
        console.log("Not read");
        btn.children[1].innerHTML = "Ikke lest";
        btn.value = "Ikke lest";
    }
}

function recommend(btn) {

  console.log("Pushing recommend-button")
  glyph = btn.children[0];

  /* Not recomended yet */
  if (glyph.classList.contains("glyphicon-star-empty")) {
    glyph.classList.remove("glyphicon-star-empty");
    glyph.classList.add("glyphicon-star");
    btn.children[1].innerHTML = "Anbefalt";
    btn.value = "Anbefalt";
  }
  /* Recommended */
  else if (glyph.classList.contains("glyphicon-star")) {
    glyph.classList.remove("glyphicon-star");
    glyph.classList.add("glyphicon-star-empty");
    btn.children[1].innerHTML = "Anbefal";
    btn.value = "Anbefal";
  }
}
