<script>
    import TimeRangeInput from "$lib/components/time-input/TimeRangeInput.svelte";
    import TimeInput from "$lib/components/time-input/TimeInput.svelte";
</script>

<h1>And They Were Roommates</h1>
<!-- TODO: In future, submitting details will require authentication -->
<p>Enter your details below to get started. These details will be used to match you with a compatible roommate.</p>
<form>
    <fieldset>
        <legend>Basic Information</legend>
        <label>
            Name:
            <input type="text" name="name" required placeholder="e.g. John Doe" />
        </label>
        <br>

        <label>
            Student ID:
            <input type="text" name="student-id" required placeholder="e.g. s1234567" />
        </label>
        <br>

        <label>
            Gender:
            <select name="gender" required>
                <option value="" disabled selected>Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="non-binary">Non-binary</option>
                <option value="prefer-not-to-say">Prefer not to say</option>
            </select>
        </label>
    </fieldset>

    <fieldset>
        <legend>Timings</legend>

        <label>
            I am likely to only work between
            <TimeRangeInput lowerTimeName="work-start" upperTimeName="work-end" />
        </label>
        <br>

        <label>
            On a night out I would go to bed at
            <TimeInput name="night-out-bedtime" defaultValue={47} />
        </label>
        <br>

        <label>
            On a quiet weekday I would go to bed at
            <TimeInput name="quiet-weekday-bedtime" defaultValue={42} />
        </label>
        <br>

        <label>
            On a normal weekday I would go to bed at
            <TimeInput name="normal-weekday-bedtime" defaultValue={42} />
        </label>
        <br>

        <label>
            I would
            <select name="overnight-guests" required>
                <option value="" disabled selected>(mind having?)</option>
                <option value="yes">be fine with</option>
                <option value="rather-no">rather avoid</option>
                <option value="no">not want</option>
            </select>
            people staying overnight
        </label>
    </fieldset>

    <fieldset>
        <legend>Personality</legend>

        <label>
            I consider myself to be an
            <select name="introvert-extrovert" required>
                <option value="" disabled selected>(introvert/extrovert?)</option>
                <option value="introvert">introvert</option>
                <option value="ambivert">ambivert</option>
                <option value="extrovert">extrovert</option>
                <option value="not-sure">not sure</option>
            </select>
        </label>
        <br>

        <label>
            I consider myself to be
            <select name="tidiness" required>
                <option value="" disabled selected>(tidy/messy?)</option>
                <option value="5">very tidy</option>
                <option value="4">somewhat tidy</option>
                <option value="3">neither tidy nor messy</option>
                <option value="2">somewhat messy</option>
                <option value="1">very messy</option>
            </select>
        </label>
        <br>

        <label>
            I
            <select name="care-about-tidiness" required>
                <option value="" disabled selected>(care about/don't care about?)</option>
                <option value="5">care a lot about</option>
                <option value="4">care somewhat about</option>
                <option value="3">neither care nor don't care about</option>
                <option value="2">don't care much about</option>
                <option value="1">don't care at all about</option>
            </select>
            my roommate's tidiness
        </label>
        <br>

        <!-- In future, these multi-text inputs could be tag-style inputs -->
        <label>
            I watch the following sports: (separate with commas)
            <input type="text" name="sports-watched" placeholder="e.g. football, basketball" />
        </label>
        <br>

        <label>
            I play the following sports: (separate with commas)
            <input type="text" name="sports-played" placeholder="e.g. tennis, swimming" />
        </label>
        <br>

        <label>
            I like the following music genres: (separate with commas)
            <input type="text" name="music-genres" placeholder="e.g. rock, classical" />
        </label>
        <br>

        <label>
            I like the following music artists: (separate with commas)
            <input type="text" name="music-artists" placeholder="e.g. The Beatles, Beyoncé" />
        </label>
        <br>

        <label>
            I would describe myself as:
            <br>
            <textarea name="self-description" rows="4" cols="50" placeholder="e.g. friendly, studious, tidy"></textarea>
        </label>
        <br>

        <label>
            My ideal roommate would describe themselves as:
            <br>
            <textarea name="ideal-roommate-description" rows="4" cols="50" placeholder="e.g. respectful, outgoing, clean"></textarea>
        </label>
    </fieldset>

    <button type="submit">Submit!</button>
</form>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Momo+Trust+Display&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Momo+Trust+Display&family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap');

    :global(body) {
        background-color: #DEE2B1;
        overflow-x: hidden;
    }

    form, h1, p {
        text-align: center;
        font-family: "Open Sans", sans-serif;
    }

    h1 {
        color: #155332;
        font-family: "Momo Trust Display", sans-serif;
    }

    fieldset {
        margin: .5em;
        border: 1px solid black;
        display: flex;
        flex-direction: column;
        align-items: center;
        overflow-x: auto;
        min-width: 0;
        box-sizing: border-box;
    }

    legend {
        font-weight: bold;
        font-size: 1.2em;
    }

    input::placeholder,
    textarea::placeholder,
    select:has(> option[value=""]:checked) {
        color: #c90000;
        font-style: italic;
    }

    button {
        font-size: 1.8em;
        padding: .3em;
        margin: .3em;
        border-radius: 1em;
    }
</style>
